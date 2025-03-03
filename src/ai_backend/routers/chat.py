# src/ai_backend/routers/chat.py

from fastapi import APIRouter
from pydantic import BaseModel
from ai_backend.services.llm_service import generate_response
from ai_backend.services.supabase_service import generate_rag_response

router = APIRouter()


class ChatRequest(BaseModel):
    prompt: str


@router.post("/generate/")
async def generate_chat(request: ChatRequest):
    """Generate response using OpenAI LLM via LangChain."""
    response = generate_response(request.prompt)
    return {"response": response}


@router.post("/generate/rag/")
async def generate_rag_chat(request: ChatRequest):
    """Retrieves relevant documents from Supabase and uses them to generate a response."""
    response = generate_rag_response(request.prompt)
    return {"response": response}
