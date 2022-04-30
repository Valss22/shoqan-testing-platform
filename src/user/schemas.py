from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, validator
from starlette import status
from starlette.responses import JSONResponse

from src.user_profile.schemas import UserProfileOut


class UserIn(BaseModel):
    email: EmailStr
    password: Optional[str]

    # @validator("email")
    # def check_email(cls, email):
    #     return JSONResponse({
    #         "detail": "Неверный email"
    #     }, status.HTTP_400_BAD_REQUEST)


class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    token: str
    is_admin: bool = Field(alias="isAdmin")
