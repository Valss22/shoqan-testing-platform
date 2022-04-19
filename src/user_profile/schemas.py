from pydantic import BaseModel

from src.user_profile.types import Specialties, Courses


class UserProfileIn(BaseModel):
    fullname: str
    specialty: Specialties
    course: Courses


class UserProfileOut(BaseModel):
    fullname: str
    specialty: Specialties
    course: Courses
    photo: str