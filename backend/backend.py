"""Backend Server Exists here"""
from fastapi import FastAPI
from routers import chat, screenshot, game_detection, settings

app = FastAPI()

app.include_router(chat.router, tags=["Chat"])
app.include_router(screenshot.router, prefix="/screenshots", tags=["Screenshots"])
app.include_router(game_detection.router, prefix="/games", tags=["Game Detection"])
app.include_router(settings.router, prefix="/settings", tags=["Settings"])