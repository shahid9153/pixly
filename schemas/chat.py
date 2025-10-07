from pydantic import BaseModel
from typing import Optional, List

class ChatMessage(BaseModel):
    message: str
    image_data: Optional[str] = None