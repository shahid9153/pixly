from pydantic import BaseModel
from typing import Optional, List
class ApiKeyRequest(BaseModel):
    api_key: str