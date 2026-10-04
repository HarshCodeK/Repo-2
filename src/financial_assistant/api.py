import os
from fastapi import FastAPI
from .answer import GroundedAnswerer
from .llm import GroqClient
from .models import AskRequest, AskResponse, ImageRequest, ImageResponse
from .retrieval import ChromaRetriever, SentenceTransformerEmbedder
from .store import InteractionStore

app = FastAPI(title="Multimodal Financial Assistant", version="0.1.0")

_retriever = None
_answerer = None
_store = None
_vision_client = None

def configure(retriever, answerer, store=None, vision_client=None):
    global _retriever, _answerer, _store, _vision_client
    _retriever, _answerer, _store, _vision_client = retriever, answerer, store, vision_client

def _ensure_dependencies():
    global _retriever, _answerer, _store, _vision_client
    if _retriever is None:
        _retriever = ChromaRetriever(os.getenv("CHROMA_DIR", "./.chroma"), SentenceTransformerEmbedder(os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")))
    if _answerer is None:
        _answerer = GroundedAnswerer(GroqClient())
    if _store is None:
        _store = InteractionStore(os.getenv("SQLITE_PATH", "./data/interactions.db"))
    if _vision_client is None:
        _vision_client = GroqClient()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    _ensure_dependencies()
    result = _answerer.answer(request.question, _retriever.search(request.question))
    _store.record(request.question, result.supported, result.answer)
    return result

@app.post("/describe-image", response_model=ImageResponse)
def describe_image(request: ImageRequest):
    _ensure_dependencies()
    return ImageResponse(answer=_vision_client.describe_image(request.question, request.image_data_url))
