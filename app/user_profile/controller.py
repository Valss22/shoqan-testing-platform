from typing import Optional

from fastapi import APIRouter, File, Depends, Body, UploadFile, Header
from app.user_profile.enums import Specialties, Courses
from app.user_profile.service import UserProfileService

user_profile_router = APIRouter(
    prefix='/user/profile'
)


@user_profile_router.post('/')
async def write_to_user_profile(
        fullname: str = Body(...),
        specialty: Specialties = Body(...),
        course: Courses = Body(...),
        photo: UploadFile = File(...),
        Authorization: str = Header(None),
        user_profile_service: UserProfileService = Depends()
):
    return await user_profile_service.write_to_user_profile(
        fullname=fullname, specialty=specialty,
        course=course, photo=photo, auth_header=Authorization
    )
