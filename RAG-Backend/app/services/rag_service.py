# app/services/rag_service.py
import logging
from typing import Dict, List, Any, Tuple, Optional

from langchain.chains import RetrievalQA
# --- NEW: Import PromptTemplate ---
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from ..core.config import settings
from .file_processor import vector_store, embedding_function
from ..db import schemas
from ..dependencies import UserQueryContext


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- LLM Initialization (Keep as is) ---
llm = None
if settings.GOOGLE_API_KEY:
    try:
        llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_CHAT_MODEL, # Ensure this uses "gemini-1.5-flash" or similar
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.2, # Low temperature for more factual RAG answers
            convert_system_message_to_human=True
        )
        logger.info(f"RAG Service: Initialized ChatGoogleGenerativeAI with model: {settings.GEMINI_CHAT_MODEL}")
    except Exception as e:
        logger.exception(f"RAG Service: Failed to initialize Google Gemini LLM: {e}")
else:
    logger.warning("RAG Service: GOOGLE_API_KEY not set. Google Gemini LLM cannot be initialized.")

# --- NEW: Define Custom Prompt Template ---
# This template instructs the LLM on how to behave.
custom_prompt_template_str = """You are a helpful assistant. Use only the following pieces of context to answer the question at the end.
If you don't know the answer from the context, you MUST say "Sorry, I don't know the answer, Please clarify your question so I can help better 🤔. but if you answer it dont include this text ever"
Do not try to make up an answer if it's not in the context.
Keep your answers concise and directly related to the question based on the provided context.
If possible, try to answer in the same language as the question.
be friendly and include emojis in your answers.

Context:
{context}

Question: {question}

Helpful Answer:"""

QA_CHAIN_PROMPT = PromptTemplate.from_template(custom_prompt_template_str)


# --- Contextual Retriever Function (Keep as is) ---
def get_contextual_retriever(user_context: UserQueryContext) -> Optional[BaseRetriever]:
    if not vector_store:
        logger.error("RAG Service: Vector store is not initialized. Cannot create retriever.")
        return None
    search_kwargs = {"k": 5}
    allowed_access_targets = []
    if user_context.role == "admin":
        logger.info("RAG Service: Admin user, retriever will not filter by doc_access_target.")
    elif user_context.role == "student":
        allowed_access_targets.append("public")
        allowed_access_targets.append("all_students")
        if user_context.level:
            allowed_access_targets.append(f"level_{user_context.level}")
        logger.info(f"RAG Service: Student (Level: {user_context.level}), allowed targets: {allowed_access_targets}")
    else: # Guest user
        allowed_access_targets.append("public")
        logger.info(f"RAG Service: Guest user, allowed targets: {allowed_access_targets}")

    if allowed_access_targets:
        metadata_filter = {"doc_access_target": {"$in": allowed_access_targets}}
        search_kwargs["filter"] = metadata_filter
        logger.info(f"RAG Service: Applying metadata filter to retriever: {metadata_filter}")
    
    try:
        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs=search_kwargs
        )
        logger.info(f"RAG Service: Retriever configured with search_kwargs: {search_kwargs}")
        return retriever
    except Exception as e:
        logger.exception(f"RAG Service: Failed to create retriever: {e}")
        return None

# --- Source Document Processing (Keep as is) ---
def process_source_documents(source_docs: List[Document]) -> List[schemas.SourceDocumentInfo]:
    processed_sources = []
    seen_sources = set()
    for doc in source_docs:
        filename = doc.metadata.get("source_filename", "Unknown Filename")
        page_num = doc.metadata.get("page_number", None)
        source_key = f"{filename}_p{page_num}"
        if source_key not in seen_sources:
            source_info = schemas.SourceDocumentInfo(
                filename=filename,
                page_number=page_num,
                metadata=doc.metadata
            )
            processed_sources.append(source_info)
            seen_sources.add(source_key)
    return processed_sources

# --- RAG Query Function (Modified to use the custom prompt) ---
def get_rag_answer(query: str, user_context: UserQueryContext) -> Tuple[str, List[schemas.SourceDocumentInfo]]:
    if not llm:
        logger.error("RAG Service: LLM is not available.")
        return "Error: The question answering system's LLM is not available.", []
    if not embedding_function:
        logger.error("RAG Service: Embedding function is not available.")
        return "Error: The question answering system's embedding function is not available.", []

    contextual_retriever = get_contextual_retriever(user_context)
    if not contextual_retriever:
        logger.error("RAG Service: Failed to obtain a contextual retriever.")
        return "Error: Could not configure document access for your request.", []

    try:
        # --- MODIFIED: Pass the custom prompt to the chain ---
        rag_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff", # "stuff" chain type is suitable for using a custom prompt for the context and question
            retriever=contextual_retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT} # Pass the custom prompt here
        )
        logger.info(f"RAG Service: Dynamically created RAG chain with custom prompt for user context: Role='{user_context.role}', Level='{user_context.level}'")
        
        logger.info(f"RAG Service: Processing query: '{query}'")
        result: Dict[str, Any] = rag_chain.invoke({"query": query}) # 'query' is the default input key for this chain

        answer = result.get('result', "Sorry, I couldn't find an answer in the accessible documents.") # Default if 'result' key is missing
        source_docs = result.get('source_documents', [])

        logger.info(f"RAG Service: Generated answer preview: '{answer[:100]}...'")
        logger.info(f"RAG Service: Retrieved {len(source_docs)} source document chunks with applied filters.")

        processed_sources = process_source_documents(source_docs)
        return answer, processed_sources

    except Exception as e:
        logger.exception(f"RAG Service: Error during RAG chain execution for query '{query}': {e}")
        return "An error occurred while processing your question. Please try again later.", []

