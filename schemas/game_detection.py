from pydantic import BaseModel
from typing import Optional, List

class GameDetectionRequest(BaseModel):
    message: Optional[str] = None