from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chatbot import generate_chat_response

router = APIRouter()


@router.post("/query", response_model=ChatResponse)
def chat_query(payload: ChatRequest):
    return ChatResponse(response=generate_chat_response(payload.message))
