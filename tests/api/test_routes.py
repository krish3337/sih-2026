import pytest
from fastapi.testclient import TestClient
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tests.contract.test_interfaces import FakeEmbedder, FakeLLMClient
from ai_core.config import EMBEDDER_REGISTRY, LLM_REGISTRY

# Register fakes
EMBEDDER_REGISTRY["fake"] = lambda: FakeEmbedder()
LLM_REGISTRY["fake"] = lambda: FakeLLMClient()

# Set env vars to use fakes
os.environ["EMBEDDER_BACKEND"] = "fake"
os.environ["LLM_BACKEND"] = "fake"

from api.main import app, create_app

@pytest.fixture
def client():
    # FastAPI test client automatically triggers lifespan events, so the pipeline will be built using fakes!
    with TestClient(app) as c:
        yield c

def test_health_check(client):
    response = client.get("/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["pipeline_loaded"] is True
    assert data["embedder_model_id"] == "fake-embedder"

def test_recommend_happy_path(client):
    response = client.post("/v1/recommend", json={"text": "water pipes", "language_hint": "English"})
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert "explanation" in data

def test_recommend_invalid_input(client):
    response = client.post("/v1/recommend", json={"text": "   "})
    assert response.status_code == 422
    assert response.json()["code"] == "INVALID_INPUT"

def test_recommend_pdf_invalid_type(client):
    files = {"file": ("test.txt", b"Hello", "text/plain")}
    response = client.post("/v1/recommend/pdf", files=files)
    assert response.status_code == 415

def test_startup_failure():
    import importlib
    import api.main
    
    os.environ["EMBEDDER_BACKEND"] = "non-existent"
    with pytest.raises(RuntimeError):
        with TestClient(api.main.create_app()):
            pass
            
    # Revert for other tests
    os.environ["EMBEDDER_BACKEND"] = "fake"
