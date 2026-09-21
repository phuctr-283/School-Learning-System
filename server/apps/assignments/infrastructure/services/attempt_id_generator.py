import uuid


def generate_attempt_id() -> str:
    return f"ATT{uuid.uuid4().hex[:20].upper()}"