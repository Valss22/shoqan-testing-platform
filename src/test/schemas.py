from pydantic import BaseModel


class TestOut(BaseModel):
    filename: str
    passed: bool
