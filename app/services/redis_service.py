import redis
import json

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


def save_chat(session_id: str, role: str, message: str):
    data = json.dumps({"role": role, "message": message})
    r.rpush(session_id, data)


def get_chat_history(session_id: str, limit: int = 10):
    history = r.lrange(session_id, -limit, -1)
    return [json.loads(h) for h in history]

def save_booking(session_id: str, booking: dict):
    r.set(f"booking:{session_id}", json.dumps(booking))


def get_booking(session_id: str):
    data = r.get(f"booking:{session_id}")
    return json.loads(data) if data else None