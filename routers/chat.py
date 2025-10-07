from fastapi import APIRouter
from services.chatbot import chat_with_gemini
from schemas.chat import ChatMessage
router = APIRouter()

@router.post("/chat")
async def chat(message: ChatMessage):
    return await chat_with_gemini(message.message, message.image_data)