from pydantic import BaseModel
from typing import Optional, List
class KnowledgeSearchRequest(BaseModel):
    query: str
    content_types: Optional[List[str]] = None
    limit: Optional[int] = 5