from fastapi import APIRouter
from app.services.qdrant_service import client
from app.services.embedding_service import get_embedding
from groq import Groq
import os

router = APIRouter()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


@router.post("/chat")
async def chat(query: str):

    try:
        query_vector = get_embedding(query)

        results = client.query_points(
            collection_name="documents",
            query=query_vector,
            limit=3,
            with_payload=True
        )

        context_chunks = []

        for hit in results.points:
            payload = getattr(hit, "payload", None)

            if payload and "text" in payload:
                context_chunks.append(payload["text"])

        context = "\n\n".join(context_chunks)

        prompt = f"""
You are a helpful AI assistant.

Use ONLY the context below to answer the question.
If the answer is not in the context, say "I don't know based on the document."

Context:
{context}

Question:
{query}

Answer clearly and concisely.
"""

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content
        
        return {
            "query": query,
            "answer": answer,
            "sources_found": len(results.points),
            "context_used": context[:300]
        }

    except Exception as e:
        return {
            "error": str(e)
        }