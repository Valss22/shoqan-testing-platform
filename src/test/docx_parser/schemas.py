from pydantic import BaseModel


class PassTestIn(BaseModel):
    answers: list[str]


class PassTestOut(BaseModel):
    score: int
    passed: bool
