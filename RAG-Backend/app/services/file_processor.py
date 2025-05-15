# app/services/file_processor.py
import io
import logging
import uuid
import os
from typing import List, Dict, Any

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

from ..core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Embedding Function and Vector Store Initialization (Keep as is) ---
embedding_function = None
try:
    embedding_function = HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL_NAME,
        model_kwargs={'device': 'cpu', 'trust_remote_code': True},
        encode_kwargs={'normalize_embeddings': True}
    )
    logger.info(f"Initialized HuggingFaceEmbeddings with model: {settings.EMBEDDING_MODEL_NAME}")
except Exception as e:
    logger.exception(f"Failed to initialize embedding model {settings.EMBEDDING_MODEL_NAME}: {e}")

vector_store = None
if embedding_function:
    try:
        os.makedirs(settings.CHROMA_DB_PATH, exist_ok=True)
        vector_store = Chroma(
            collection_name=settings.VECTOR_DB_COLLECTION_NAME,
            embedding_function=embedding_function,
            persist_directory=settings.CHROMA_DB_PATH
        )
        logger.info(f"Initialized ChromaDB client. Data path: {settings.CHROMA_DB_PATH}, Collection: {settings.VECTOR_DB_COLLECTION_NAME}")
    except Exception as e:
        logger.exception(f"Failed to initialize ChromaDB vector store: {e}")
        vector_store = None
else:
    logger.warning("Embedding function not available, ChromaDB vector store not initialized.")

# --- Document Loading and Splitting (Keep load_document and split_documents as is) ---
def load_document(file_content: bytes, file_type: str, original_filename: str) -> List[Any]:
    # ... (your existing load_document code)
    docs = []
    temp_file_path = f"./temp_{uuid.uuid4()}" # Base temp name
    try:
        if file_type == "application/pdf":
            temp_file_path += ".pdf"
            with open(temp_file_path, "wb") as f_out: f_out.write(file_content)
            loader = PyPDFLoader(temp_file_path)
            docs = loader.load()
        elif file_type in ["text/plain", "text/markdown", "text/csv"]:
            temp_file_path += ".txt"
            with open(temp_file_path, "wb") as f_out: f_out.write(file_content)
            loader = TextLoader(temp_file_path, encoding='utf-8')
            docs = loader.load()
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            temp_file_path += ".docx"
            with open(temp_file_path, "wb") as f_out: f_out.write(file_content)
            loader = Docx2txtLoader(temp_file_path)
            docs = loader.load()
        else:
            logger.warning(f"Unsupported file type: {file_type} for file: {original_filename}")
            return []

        for doc in docs:
            doc.metadata = doc.metadata or {}
            doc.metadata["source_filename"] = original_filename
        logger.info(f"Loaded {len(docs)} pages/documents from {original_filename}")
        return docs
    except Exception as e:
        logger.error(f"Error loading file {original_filename} (type: {file_type}): {e}", exc_info=True)
        return []
    finally:
        if os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except OSError as e:
                 logger.error(f"Error removing temporary file {temp_file_path}: {e}")

def split_documents(docs: List[Any]) -> List[Any]:
    # ... (your existing split_documents code)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        length_function=len,
        add_start_index=True,
    )
    split_docs = text_splitter.split_documents(docs)
    logger.info(f"Split {len(docs)} documents into {len(split_docs)} chunks.")
    return split_docs

# --- MODIFIED: process_and_embed_document to include doc_access_target ---
def process_and_embed_document(
    file_content: bytes,
    file_type: str,
    original_filename: str,
    doc_access_target: str # <-- New parameter
) -> str | None:
    if vector_store is None or embedding_function is None:
        logger.error("Vector store or embedding function not initialized. Cannot process document.")
        raise RuntimeError("System not properly configured for embedding. Check logs.")

    doc_internal_id = f"doc_{uuid.uuid4()}"
    logger.info(f"Processing document: {original_filename} (Internal ID: {doc_internal_id}), Access Target: {doc_access_target}")

    try:
        loaded_docs = load_document(file_content, file_type, original_filename)
        if not loaded_docs:
            logger.warning(f"Loading returned no documents for: {original_filename}")
            return None

        split_docs = split_documents(loaded_docs)
        if not split_docs:
            logger.warning(f"No chunks generated after splitting document: {original_filename}")
            return None

        for i, doc_chunk in enumerate(split_docs):
            doc_chunk.metadata = doc_chunk.metadata or {}
            doc_chunk.metadata["source_filename"] = doc_chunk.metadata.get("source_filename", original_filename)
            doc_chunk.metadata["page_number"] = doc_chunk.metadata.get("page", None)
            doc_chunk.metadata["doc_internal_id"] = doc_internal_id
            doc_chunk.metadata["chunk_index"] = i
            # --- NEW: Add access target to metadata ---
            doc_chunk.metadata["doc_access_target"] = doc_access_target
            doc_chunk.metadata.pop('source', None) # Remove temp file path if it exists

        texts = [doc.page_content for doc in split_docs]
        metadatas = [doc.metadata for doc in split_docs]
        ids = [f"{doc_internal_id}_chunk_{i}" for i in range(len(split_docs))]

        logger.info(f"Adding {len(split_docs)} chunks to Chroma for document ID: {doc_internal_id}")
        vector_store.add_texts(texts=texts, metadatas=metadatas, ids=ids)
        logger.info(f"Successfully added chunks for document {original_filename} (ID: {doc_internal_id}).")
        return doc_internal_id

    except Exception as e:
        logger.exception(f"Failed during processing/embedding of {original_filename}: {e}")
        raise
