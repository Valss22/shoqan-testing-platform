from pydantic import BaseModel, EmailStr


class UserIn(BaseModel):
    email: EmailStr

