from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    # --- API Keys (Required) ---
    OPENAI_API_KEY: str
    PINECONE_API_KEY: str
    
    # --- Vector Database Settings ---
    PINECONE_INDEX_NAME: str = "lt-project-alpha"
    
    # --- API & App Settings ---
    APP_ENV: str = "development"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # --- RAG Hyperparameters ---
    # Centralizing these allows us to easily tweak the AI's behavior later
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    EMBEDDING_MODEL: str = "text-embedding-3-small"  # OpenAI's fastest/cheapest embedding model
    LLM_MODEL: str = "gpt-3.5-turbo"                 # Can swap to gpt-4 or gpt-4o later
    TEMPERATURE: float = 0.0                         # 0.0 ensures factual, non-hallucinated answers

    # Tell Pydantic to look for the .env file
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache()
def get_settings() -> Settings:
    """
    Uses lru_cache to ensure we only read the .env file once upon startup.
    This is a Singleton pattern for performance.
    """
    return Settings()