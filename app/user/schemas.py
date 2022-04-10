from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserIn(BaseModel):
    email: EmailStr
    password: Optional[str]


class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    token: str
