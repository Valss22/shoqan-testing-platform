from typing import Optional

from pydantic import BaseModel


class TestOut(BaseModel):
    filename: str
    passed: Optional[bool]
