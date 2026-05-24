from pydantic import BaseModel, Field
from typing import List, Optional

class DocumentMetadata(BaseModel):
    """
    Schema to standardize the metadata attached to every vector in Pinecone.
    Prevents missing citations later.
    """
    source_file: str
    chunk_id: str
    page_number: Optional[int] = None

class ProjectInsight(BaseModel):
    """
    The strict JSON schema that the LLM MUST return.
    Instead of unstructured text, the LLM acts as a reasoning engine
    that fills out this exact data structure.
    """
    answer: str = Field(
        description="The direct, objective answer to the user's question based strictly on the retrieved context."
    )
    evidence_citations: List[str] = Field(
        description="List of exact document names and lines used to formulate the answer. Must not be empty if an answer is provided."
    )
    risk_score: float = Field(
        description="A calculated risk score from 0.0 (No Risk) to 1.0 (Critical Delay/Financial Impact)."
    )
    responsible_owner: str = Field(
        description="The specific name, role, or vendor responsible for the issue, if mentioned in the text."
    )
    next_action: str = Field(
        description="The recommended escalation or corrective action based on project guidelines or meeting minutes."
    )