from fastapi.testclient import TestClient
from financial_assistant.api import app, configure
from financial_assistant.models import RetrievedChunk, SourceType, Answer
from unittest.mock import patch

class FakeRetriever:
    def search(self, question):
        return [RetrievedChunk(source="policy.pdf", source_type=SourceType.pdf, text="Meals are reimbursed up to 500 INR.", page=3, distance=.1)]
class FakeAnswerer:
    def answer(self, question, evidence):
        return Answer(supported=True, answer="Meals are reimbursed up to 500 INR.", sources=evidence)
class FakeStore:
    def __init__(self): self.rows=[]
    def record(self, question, supported, answer): self.rows.append((question,supported,answer))

def test_health_and_ask():
    store=FakeStore(); configure(FakeRetriever(), FakeAnswerer(), store)
    client=TestClient(app)
    assert client.get("/health").json()=={"status":"ok"}
    response=client.post("/ask", json={"question":"What is the meal limit?"})
    assert response.status_code==200
    assert response.json()["supported"] is True
    assert len(store.rows)==1

def test_describe_image():
    configure(FakeRetriever(), FakeAnswerer(), FakeStore())
    client=TestClient(app)
    with patch("financial_assistant.api.GroqClient.describe_image", return_value="The image shows a 500 INR meal limit.") as mocked:
        response=client.post("/describe-image", json={"question":"What is shown?", "image_data_url":"data:image/jpeg;base64,AAAA"})
    assert response.status_code==200
    assert "500 INR" in response.json()["answer"]
    mocked.assert_called_once()

def test_image_rejects_non_image_data_url():
    configure(FakeRetriever(), FakeAnswerer(), FakeStore())
    client = TestClient(app)
    response = client.post("/describe-image", json={"question": "What is shown?", "image_data_url": "data:text/plain;base64,AAAA"})
    assert response.status_code == 422
