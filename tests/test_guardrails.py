import pytest
from pydantic import ValidationError
from src.guardrails import ProjectInsight

def test_valid_project_insight():
    """Test that a correctly formatted LLM response passes validation."""
    valid_data = {
        "answer": "The concrete pouring is delayed by 3 weeks.",
        "evidence_citations": ["04_MOM_Project_Review.txt"],
        "risk_score": 0.85,
        "responsible_owner": "Global Steel Suppliers",
        "next_action": "Enforce 2% penalty."
    }
    
    insight = ProjectInsight(**valid_data)
    assert insight.risk_score == 0.85
    assert insight.responsible_owner == "Global Steel Suppliers"

def test_invalid_project_insight_types():
    """Test that guardrails block invalid data types (e.g., hallucinated schema)."""
    invalid_data = {
        "answer": "The concrete pouring is delayed.",
        "evidence_citations": ["04_MOM_Project_Review.txt"],
        "risk_score": "CRITICAL",  # This should fail. Pydantic expects a float.
        "responsible_owner": "Global Steel Suppliers",
        "next_action": "Enforce 2% penalty."
    }
    
    # We expect Pydantic to raise a ValidationError here
    with pytest.raises(ValidationError):
        ProjectInsight(**invalid_data)