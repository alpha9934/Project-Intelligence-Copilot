import os
import time
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from src.config import get_settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)
settings = get_settings()

def get_vector_store() -> PineconeVectorStore:
    """
    Initializes the connection to Pinecone and sets up the OpenAI Embedding model.
    """
    # --- THE FIX: Inject Pydantic settings into global environment for LangChain ---
    os.environ["PINECONE_API_KEY"] = settings.PINECONE_API_KEY
    os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

    logger.info(f"Connecting to Pinecone index: {settings.PINECONE_INDEX_NAME}...")
    
    # 1. Initialize Pinecone Client
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    
    # 2. Check if index exists; if not, create it defensively
    existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
    
    if settings.PINECONE_INDEX_NAME not in existing_indexes:
        logger.warning(f"Index '{settings.PINECONE_INDEX_NAME}' not found. Provisioning a new serverless index...")
        
        pc.create_index(
            name=settings.PINECONE_INDEX_NAME,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1" 
            )
        )
        
        while not pc.describe_index(settings.PINECONE_INDEX_NAME).status['ready']:
            logger.info("Waiting for Pinecone index to be ready...")
            time.sleep(2)
            
        logger.info(f"Index '{settings.PINECONE_INDEX_NAME}' created successfully.")

    # 3. Initialize OpenAI Embeddings (It will now read from os.environ automatically)
    embeddings = OpenAIEmbeddings(
        model=settings.EMBEDDING_MODEL
    )
    
    # 4. Return the LangChain Vector Store abstraction
    vector_store = PineconeVectorStore.from_existing_index(
        index_name=settings.PINECONE_INDEX_NAME,
        embedding=embeddings
        # (Removed the pinecone_api_key line that caused the error)
    )
    
    logger.info("Vector store connection established successfully.")
    return vector_store