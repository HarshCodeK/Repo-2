# Architecture

## Goal
Answer questions about financial policies from supplied evidence and refuse unsupported questions.

## Flow
1. PDF text is extracted into page-aware chunks.
2. Images are validated and converted to a data URL for the vision endpoint.
3. Text chunks are embedded and stored in ChromaDB.
4. A question retrieves the closest chunks.
5. The LLM receives only retrieved evidence and is instructed to stay grounded.
6. SQLite records the interaction; it is not the retrieval store.

## Why ChromaDB over SQL
Semantic retrieval is the core query: find passages close to a question in embedding space. ChromaDB provides a simple persistent vector collection without implementing vector storage, indexing, and distance search ourselves. SQLite remains a better fit for structured interaction logs where exact filtering and durability matter.

## Why sentence-transformers
The embedding model runs locally, avoiding an additional embedding API dependency and keeping the retrieval boundary explicit. `all-MiniLM-L6-v2` is small enough for a portfolio project and replaceable behind the `Embedder` protocol.

## Why FastAPI
The API creates a clean boundary between the service and the Streamlit demo, and it is easy to test with dependency injection.

## Grounding contract
The text-answer provider must return structured JSON containing `supported` and `answer`. Pydantic validates that response before it becomes an API response. When `supported=false`, retrieved sources are omitted from the answer so the UI does not present unsupported passages as citations. This reduces accidental overclaiming but is not a formal hallucination guarantee.

## Image boundary
Images use a separate vision endpoint rather than being silently inserted into the text retrieval index. The API validates the data-URL media type and size before passing it to the vision provider. This keeps the multimodal path explicit and avoids pretending that image-derived facts have the same provenance as indexed PDF text.

## Design boundary
The project does not claim financial advice, transaction execution, compliance certification, or production-grade document governance.
