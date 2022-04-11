from pydantic import BaseModel

from app.user_profile.types import University


class UserProfileIn(BaseModel):

    full_name: str
    university: University
