from qdrant_client.models import VectorParams, Distance
from app.services.qdrant_service import client

client.recreate_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)

print("Collection created successfully")