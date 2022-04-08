from pydantic import BaseModel


class UserIn(BaseModel):
    email: str
