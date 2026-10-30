from typing import Literal
from pydantic import BaseModel, Field


class Query(BaseModel):
    message: str = Field(min_length=1, max_length=8000, pattern=r"\S")


class Route(BaseModel):
    agent: Literal["visa", "career", "clarify"]
    reason: str


class Citation(BaseModel):
    id: str
    title: str
    url: str
    reviewed: str
    excerpt: str


class Answer(BaseModel):
    agent: Literal["visa", "career", "clarify"]
    answer: str
    citations: list[Citation] = Field(default_factory=list)
    model: str
