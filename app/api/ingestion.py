from fastapi import APIRouter, UploadFile, File, HTTPException, Form
import os
from app.services.embedding_service import get_embedding
from app.services.qdrant_service import client
from qdrant_client.models import PointStruct
import uuid

from app.services.document_processor import (
    extract_text_from_pdf,
    extract_text_from_txt
)

from app.services.chunking import (
    fixed_chunking,
    recursive_chunking
)

router = APIRouter()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/ingest")
async def ingest_file(
    file: UploadFile = File(...),
    chunking_strategy: str = Form(...)
):
    extension = file.filename.split(".")[-1].lower()

    if extension not in ["pdf", "txt"]:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are allowed."
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    if extension == "pdf":
        text = extract_text_from_pdf(file_path)
    else:
        text = extract_text_from_txt(file_path)

    if chunking_strategy == "fixed":
        chunks = fixed_chunking(text)
    elif chunking_strategy == "recursive":
        chunks = recursive_chunking(text)
    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid chunking strategy."
        )

    points = []

    for i, chunk in enumerate(chunks):
        vector = get_embedding(chunk)

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "filename": file.filename,
                    "chunk_index": i,
                    "text": chunk,
                    "chunking_strategy": chunking_strategy
                }
            )
        )

    client.upsert(
        collection_name="documents",
        points=points
    )

    return {
        "filename": file.filename,
        "characters": len(text),
        "chunking_strategy": chunking_strategy,
        "number_of_chunks": len(chunks),
        "stored_vectors": len(points),
        "message": "Chunks embedded and stored in Qdrant successfully"
    }