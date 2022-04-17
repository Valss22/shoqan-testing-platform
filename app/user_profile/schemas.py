from pydantic import BaseModel

from app.user_profile.enums import Specialties, Courses


class UserProfileIn(BaseModel):
    fullname: str
    specialty: Specialties
    course: Courses


class UserProfileOut(BaseModel):
    fullname: str
    specialty: Specialties
    course: Courses
    photo: str
