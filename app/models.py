from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class Query(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    citations: Optional[List[Dict[str, Any]]] = []

class ErrorResponse(BaseModel):
    error: str
