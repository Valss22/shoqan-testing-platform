from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TestOut(BaseModel):
    id: UUID
    filename: str
    passed: Optional[bool]