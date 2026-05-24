from fastapi.testclient import TestClient
from src.main import app

# Create a test client that bypasses the actual network layer
client = TestClient(app)

def test_health_check():
    """Test that the API is alive and responding to load balancers."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "Project Intelligence Copilot"}

def test_ask_endpoint_missing_payload():
    """Test that the API rejects requests missing required fields."""
    # We are missing the 'question' field in this payload
    bad_payload = {
        "project_id": "project_alpha"
    }
    
    response = client.post("/ask", json=bad_payload)
    
    # 422 is FastAPI's standard code for 'Unprocessable Entity' (Validation Error)
    assert response.status_code == 422