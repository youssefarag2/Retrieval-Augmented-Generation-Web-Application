# app/services/rag_service.py
import logging
from typing import Dict, List, Any, Tuple, Optional

from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever # For type hinting

from ..core.config import settings
from .file_processor import vector_store, embedding_function
from ..db import schemas
# --- NEW: Import UserQueryContext for type hinting ---
from ..dependencies import UserQueryContext


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- LLM Initialization (Keep as is) ---
llm = None
if settings.GOOGLE_API_KEY:
    try:
        llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_CHAT_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.2,
            convert_system_message_to_human=True
        )
        logger.info(f"RAG Service: Initialized ChatGoogleGenerativeAI with model: {settings.GEMINI_CHAT_MODEL}")
    except Exception as e:
        logger.exception(f"RAG Service: Failed to initialize Google Gemini LLM: {e}")
else:
    logger.warning("RAG Service: GOOGLE_API_KEY not set. Google Gemini LLM cannot be initialized.")


# --- RAG Chain Initialization (Modified to build retriever dynamically) ---
# We will not initialize rag_chain globally anymore,
# as the retriever needs to be context-dependent.

def get_contextual_retriever(user_context: UserQueryContext) -> Optional[BaseRetriever]:
    """
    Creates a ChromaDB retriever with metadata filters based on user context.
    """
    if not vector_store:
        logger.error("RAG Service: Vector store is not initialized. Cannot create retriever.")
        return None

    # Define base search_kwargs
    search_kwargs = {"k": 5} # Retrieve top 5 relevant chunks

    # --- Build metadata filter based on user_context ---
    # ChromaDB's $or operator is used for multiple allowed values for a field.
    # Example filter: {"$and": [{"source": "source1"}, {"word_count": {"$gte": 20}}]}
    # Example filter for "field is one of [A, B, C]": {"field": {"$in": ["A", "B", "C"]}}
    
    allowed_access_targets = []

    if user_context.role == "admin":
        # Admins can access everything, so no specific doc_access_target filter needed,
        # or they can access all targets. For simplicity, let's assume they bypass this filter.
        # If you want admins to only see "admin_only" and public, adjust accordingly.
        # For now, let's let them see all documents by not applying a filter on doc_access_target.
        logger.info("RAG Service: Admin user, retriever will not filter by doc_access_target.")
        # No specific filter means all documents are considered based on similarity.
        # If you wanted to restrict admins to *only* "admin_only" docs, you would add:
        # allowed_access_targets.append("admin_only")
        # And then build the filter as below. For now, no filter for admin.

    elif user_context.role == "student":
        allowed_access_targets.append("public")
        allowed_access_targets.append("all_students")
        if user_context.level:
            allowed_access_targets.append(f"level_{user_context.level}")
        logger.info(f"RAG Service: Student (Level: {user_context.level}), allowed targets: {allowed_access_targets}")
    
    else: # Guest user
        allowed_access_targets.append("public")
        logger.info(f"RAG Service: Guest user, allowed targets: {allowed_access_targets}")

    # If there are specific targets to filter by (not admin or if admin has specific targets)
    if allowed_access_targets: # This will be true for students and guests
        # Important: ChromaDB metadata filter structure
        # To filter where 'doc_access_target' is one of the values in allowed_access_targets:
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
    # ... (your existing process_source_documents code)
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

# --- RAG Query Function (Modified) ---
def get_rag_answer(query: str, user_context: UserQueryContext) -> Tuple[str, List[schemas.SourceDocumentInfo]]:
    """
    Uses the RAG chain to get an answer and the source documents,
    applying access control based on user_context.
    """
    if not llm:
        logger.error("RAG Service: LLM is not available.")
        return "Error: The question answering system's LLM is not available.", []
    if not embedding_function: # Should also check this
        logger.error("RAG Service: Embedding function is not available.")
        return "Error: The question answering system's embedding function is not available.", []

    # Get a retriever configured for the current user's context
    contextual_retriever = get_contextual_retriever(user_context)
    if not contextual_retriever:
        logger.error("RAG Service: Failed to obtain a contextual retriever.")
        return "Error: Could not configure document access for your request.", []

    try:
        # Create the RAG chain dynamically with the contextual retriever
        rag_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=contextual_retriever,
            return_source_documents=True,
        )
        logger.info(f"RAG Service: Dynamically created RAG chain for user context: Role='{user_context.role}', Level='{user_context.level}'")
        
        logger.info(f"RAG Service: Processing query: '{query}'")
        result: Dict[str, Any] = rag_chain.invoke({"query": query})

        answer = result.get('result', "Sorry, I couldn't find an answer in the accessible documents.")
        source_docs = result.get('source_documents', [])

        logger.info(f"RAG Service: Generated answer preview: '{answer[:100]}...'")
        logger.info(f"RAG Service: Retrieved {len(source_docs)} source document chunks with applied filters.")

        processed_sources = process_source_documents(source_docs)
        return answer, processed_sources

    except Exception as e:
        logger.exception(f"RAG Service: Error during RAG chain execution for query '{query}': {e}")
        return "An error occurred while processing your question. Please try again later.", []

