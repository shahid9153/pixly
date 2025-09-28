from fastapi import FastAPI
import uvicorn
from .chatbot import chat_with_gemini
from .screenshot import start_screenshot_capture, stop_screenshot_capture, get_recent_screenshots, get_screenshot_by_id, get_screenshot_stats
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

# Screenshot endpoints
@app.post("/screenshots/start")
def start_screenshots(interval: int = 30):
    """Start automatic screenshot capture."""
    start_screenshot_capture(interval)
    return {"status": "ok", "message": f"Screenshot capture started with {interval}s interval"}

@app.post("/screenshots/stop")
def stop_screenshots():
    """Stop automatic screenshot capture."""
    stop_screenshot_capture()
    return {"status": "ok", "message": "Screenshot capture stopped"}

@app.get("/screenshots/recent")
def get_recent_screenshots_endpoint(limit: int = 10, application: str = None):
    """Get recent screenshots."""
    screenshots = get_recent_screenshots(limit=limit, application=application)
    return {"status": "ok", "screenshots": screenshots}

@app.get("/screenshots/stats")
def get_screenshot_stats_endpoint():
    """Get screenshot statistics."""
    stats = get_screenshot_stats()
    return {"status": "ok", "stats": stats}

@app.get("/screenshots/{screenshot_id}")
def get_screenshot_endpoint(screenshot_id: int):
    """Get screenshot data by ID."""
    screenshot_data = get_screenshot_by_id(screenshot_id)
    if screenshot_data:
        import base64
        return {"status": "ok", "data": base64.b64encode(screenshot_data).decode('utf-8')}
    else:
        return {"status": "error", "message": "Screenshot not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
