from fastapi import FastAPI
import uvicorn
from .chatbot import chat_with_gemini
from pydantic import BaseModel
from . import app

class ChatMessage(BaseModel):
    message: str

@app.post("/chat")
async def chat(message: ChatMessage):
    return await chat_with_gemini(message.message)

@app.get("/taskA")
def run_task_a():
    return {"status": "ok", "message": "Task A executed"}

@app.get("/taskB")
def run_task_b():
    return {"status": "ok", "message": "Task B executed"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
