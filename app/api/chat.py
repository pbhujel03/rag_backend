from fastapi import APIRouter
from app.services.qdrant_service import client
from app.services.embedding_service import get_embedding
from groq import Groq
from app.services.redis_service import (
    save_chat,
    get_chat_history,
    save_booking
)
import re
import json
import uuid
import os

router = APIRouter()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# SAFE JSON EXTRACTION
def clean_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)
    return None


# BOOKING EXTRACTION
def extract_booking(text: str):
    prompt = f"""
Extract booking details from the message.

Return ONLY valid JSON:
{{
  "name": "",
  "email": "",
  "date": "",
  "time": ""
}}

If missing, use null.

Message:
{text}
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# CHAT ENDPOINT
@router.post("/chat")
async def chat(query: str, session_id: str = None):

    try:
        if not session_id:
            session_id = str(uuid.uuid4())

        save_chat(session_id, "user", query)

        history = get_chat_history(session_id)

        query_vector = get_embedding(query)

        results = client.query_points(
            collection_name="documents",
            query=query_vector,
            limit=3,
            with_payload=True
        )

        context = "\n\n".join(
            hit.payload.get("text", "")
            for hit in results.points
            if hit.payload
        )

        chat_history_text = "\n".join(
            f"{h['role']}: {h['message']}"
            for h in history
        )

        # BOOKING EXTRACTION (FIXED)
        booking_raw = extract_booking(query)

        cleaned = clean_json(booking_raw)

        booking = None

        if cleaned:
            try:
                booking = json.loads(cleaned)

                if booking.get("name") or booking.get("email"):
                    save_booking(session_id, booking)

            except:
                booking = None

        # LLM PROMPT
        prompt = f"""
You are a helpful AI assistant.

Chat History:
{chat_history_text}

Context:
{context}

User Question:
{query}

Answer clearly and use context if needed.
"""

        # LLM RESPONSE
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content

        save_chat(session_id, "assistant", answer)

        return {
            "session_id": session_id,
            "query": query,
            "answer": answer,
            "sources_found": len(results.points),
            "booking_extracted": booking
        }

    except Exception as e:
        return {
            "error": str(e)
        }