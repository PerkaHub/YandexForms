import uuid


async def generate_response_id() -> str:
    return str(uuid.uuid4())
