import pytest
chromadb = pytest.importorskip("chromadb")
from financial_assistant.models import DocumentChunk, SourceType
from financial_assistant.retrieval import ChromaRetriever

class FakeEmbedder:
    def embed(self, texts):
        return [[1.0,0.0] if "meal" in t.lower() else [0.0,1.0] for t in texts]

def test_chroma_round_trip(tmp_path):
    retriever=ChromaRetriever(str(tmp_path), FakeEmbedder(), collection_name="test")
    retriever.upsert([DocumentChunk(source="p.pdf", source_type=SourceType.pdf, text="Meal allowance is 500 INR.", page=1)])
    results=retriever.search("meal allowance", k=1)
    assert results[0].text.startswith("Meal allowance")
