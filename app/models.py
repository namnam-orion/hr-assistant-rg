from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class ChatMessage(BaseModel):
    role: str 
    content: str

class Query(BaseModel):
    messages: List[ChatMessage]

class AnswerResponse(BaseModel):
    answer: str
    citations: Optional[List[Dict[str, Any]]] = []

class ErrorResponse(BaseModel):
    error: str
