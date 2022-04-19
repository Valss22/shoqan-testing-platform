from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

from src.user_profile.schemas import UserProfileOut


class UserIn(BaseModel):
    email: EmailStr
    password: Optional[str]


class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    token: str
    is_admin: bool = Field(alias="isAdmin")
