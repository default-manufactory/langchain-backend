# src/ai_backend/routers/chat.py

from fastapi import APIRouter
from pydantic import BaseModel
from ai_backend.services.llm_service import generate_response

router = APIRouter()


class ChatRequest(BaseModel):
    prompt: str


@router.post("/generate/")
async def generate_chat(request: ChatRequest):
    """Generate response using OpenAI LLM via LangChain."""
    response = generate_response(request.prompt)
    return {"response": response}
