from pydantic import BaseModel


class UserIn(BaseModel):
    email: str


class UserOut(BaseModel):
    email: str
