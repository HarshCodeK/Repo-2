from pathlib import Path
import base64
import io
import fitz
from PIL import Image
from .models import DocumentChunk, SourceType

MAX_IMAGE_BYTES = 8 * 1024 * 1024

def extract_pdf(path: str | Path) -> list[DocumentChunk]:
    chunks: list[DocumentChunk] = []
    with fitz.open(path) as doc:
        for page_number, page in enumerate(doc, start=1):
            text = " ".join(page.get_text("text").split())
            if text:
                chunks.append(DocumentChunk(source=str(path), source_type=SourceType.pdf, text=text, page=page_number))
    return chunks

def validate_image(path: str | Path) -> Image.Image:
    raw = Path(path).read_bytes()
    if len(raw) > MAX_IMAGE_BYTES:
        raise ValueError("image is larger than the 8 MiB limit")
    image = Image.open(io.BytesIO(raw))
    image.verify()
    return Image.open(io.BytesIO(raw)).convert("RGB")

def image_bytes_as_data_url(raw: bytes) -> str:
    if len(raw) > MAX_IMAGE_BYTES:
        raise ValueError("image is larger than the 8 MiB limit")
    image = Image.open(io.BytesIO(raw))
    image.verify()
    image = Image.open(io.BytesIO(raw)).convert("RGB")
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=85)
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded}"

def image_as_data_url(path: str | Path) -> str:
    image = validate_image(path)
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=85)
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded}"

def image_description_chunk(path: str | Path, description: str) -> DocumentChunk:
    text = " ".join(description.split())
    if not text:
        raise ValueError("image description cannot be empty")
    return DocumentChunk(source=str(path), source_type=SourceType.image, text=text)
