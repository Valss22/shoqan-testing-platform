from typing import Optional

from pydantic import BaseModel


class PassTestIn(BaseModel):
    answers: list[Optional[str]]


class PassTestOut(BaseModel):
    score: int
    passed: bool
