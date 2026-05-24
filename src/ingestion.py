import os
import glob
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import get_settings
from src.utils.logger import setup_logger
from src.vector_store import get_vector_store

logger = setup_logger(__name__)
settings = get_settings()

def process_documents(raw_dir: str = "data/raw"):
    """
    Reads PDFs and TXT files from the raw directory, splits them into semantic chunks,
    enriches them with tracking metadata, and upserts them to Pinecone.
    """
    logger.info(f"Starting ingestion pipeline. Target directory: {raw_dir}")
    
    # 1. Initialize the semantic chunker using our centralized config
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )
    
    all_chunks = []
    
    # Grab all PDF and TXT files from the synthetic dataset
    file_paths = glob.glob(f"{raw_dir}/*.pdf") + glob.glob(f"{raw_dir}/*.txt")
    
    if not file_paths:
        logger.error(f"No files found in '{raw_dir}'. Please add the synthetic documents.")
        return

    # 2. Iterate through files with fault-tolerance (try/except)
    for path in file_paths:
        filename = os.path.basename(path)
        try:
            logger.info(f"Processing file: {filename}")
            
            # Route to the correct loader based on file extension
            if path.endswith(".pdf"):
                loader = PyPDFLoader(path)
            elif path.endswith(".txt"):
                loader = TextLoader(path, encoding="utf-8")
            else:
                continue
            
            # Load and split
            raw_docs = loader.load()
            chunks = text_splitter.split_documents(raw_docs)
            
            # 3. Enrich Metadata (Crucial for Guardrails and Citations later)
            for i, chunk in enumerate(chunks):
                chunk.metadata["source_file"] = filename
                chunk.metadata["chunk_id"] = f"{filename}_chunk_{i}"
                # If page numbers exist (PDFs), ensure they are integers
                if "page" in chunk.metadata:
                    chunk.metadata["page_number"] = int(chunk.metadata["page"])
                
            all_chunks.extend(chunks)
            logger.info(f"Successfully extracted {len(chunks)} chunks from {filename}")
            
        except Exception as e:
            # If one file is corrupted, log the error but don't crash the whole pipeline
            logger.error(f"Failed to process {filename}. Error: {str(e)}")
            
    # 4. Upsert to Pinecone
    if all_chunks:
        logger.info(f"Pushing {len(all_chunks)} total chunks to Pinecone index: '{settings.PINECONE_INDEX_NAME}'...")
        vector_store = get_vector_store()
        
        # LangChain's vector store handles batching automatically under the hood
        vector_store.add_documents(all_chunks)
        logger.info("✅ Ingestion complete! Data is successfully embedded and stored in Pinecone.")

if __name__ == "__main__":
    # Ensure the script runs from the project root
    if not os.path.exists("data/raw"):
        logger.warning("Creating 'data/raw' directory. Please place your files there and re-run.")
        os.makedirs("data/raw", exist_ok=True)
    else:
        process_documents()