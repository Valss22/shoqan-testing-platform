from typing import Optional
from pydantic.main import BaseModel


class StressOut(BaseModel):
    passed: bool
    test: Optional[list[dict]]


class StressIn(BaseModel):
    answers: list[str]
