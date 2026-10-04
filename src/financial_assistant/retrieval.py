from typing import Protocol
from .models import DocumentChunk, RetrievedChunk

class Embedder(Protocol):
    def embed(self, texts: list[str]) -> list[list[float]]: ...

class SentenceTransformerEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)
    def embed(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts, normalize_embeddings=True).tolist()

class ChromaRetriever:
    def __init__(self, persist_dir: str, embedder: Embedder, collection_name: str = "financial_policy"):
        import chromadb
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(collection_name)
        self.embedder = embedder

    def upsert(self, chunks: list[DocumentChunk]) -> None:
        if not chunks:
            return
        ids = [f"{i}:{c.source}:{c.page or 0}" for i, c in enumerate(chunks)]
        self.collection.upsert(
            ids=ids,
            documents=[c.text for c in chunks],
            embeddings=self.embedder.embed([c.text for c in chunks]),
            metadatas=[{"source": c.source, "source_type": c.source_type.value, "page": c.page or 0} for c in chunks],
        )

    def search(self, question: str, k: int = 4) -> list[RetrievedChunk]:
        result = self.collection.query(query_embeddings=self.embedder.embed([question]), n_results=k)
        docs = result.get("documents", [[]])[0]
        distances = result.get("distances", [[]])[0]
        metas = result.get("metadatas", [[]])[0]
        return [RetrievedChunk(text=d, distance=float(distances[i]), source=metas[i]["source"], source_type=metas[i]["source_type"], page=(metas[i].get("page") or None)) for i, d in enumerate(docs)]
