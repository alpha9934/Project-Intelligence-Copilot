from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.rag_service import answer_question
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# 1. Initialize FastAPI Application
app = FastAPI(
    title="L&T Project Intelligence Copilot",
    description="Enterprise API for infrastructure project risk analysis and RAG reasoning.",
    version="1.0.0"
)

# 2. Define Request Schema
class AskRequest(BaseModel):
    project_id: str = Field(..., description="The ID of the project (e.g., 'project_alpha')")
    question: str = Field(..., description="The user's natural language question regarding the project.")

# 3. Define Endpoints
@app.get("/")
def health_check():
    """Simple health check endpoint for load balancers/Kubernetes."""
    return {"status": "healthy", "service": "Project Intelligence Copilot"}

@app.post("/ask")
def ask_copilot(request: AskRequest):
    """
    Primary RAG endpoint. 
    Accepts a question, queries the vector database, and returns a structured Pydantic JSON response.
    """
    logger.info(f"API Request received for project '{request.project_id}'. Question: {request.question}")
    
    try:
        # Call our core RAG reasoning engine
        response = answer_question(request.question)
        return response
        
    except Exception as e:
        logger.error(f"API Error during /ask execution: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Copilot reasoning error.")