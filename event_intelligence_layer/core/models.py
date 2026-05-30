from pydantic import BaseModel
from typing import Optional


class AskRequest(BaseModel):
    question: str


class Source(BaseModel):
    type: str
    label: str


class AskResponse(BaseModel):
    answer: str
    confidence: str  # "high" | "medium" | "low"
    sources: list[Source]
    caveat: Optional[str] = None
