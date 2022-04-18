from typing import Optional

from fastapi import APIRouter, File, Depends, Body, UploadFile, Header
from app.user_profile.enums import Specialties, Courses
from app.user_profile.schemas import UserProfileIn, UserProfileOut
from app.user_profile.service import UserProfileService

user_profile_router = APIRouter(
    prefix='/user/profile'
)


@user_profile_router.post('/', response_model=UserProfileOut)
async def write_to_profile(
    user_profile: UploadFile = Body(..., alias="userProfile"),
    photo: UploadFile = File(...),
    Authorization: str = Header(None),
    user_profile_service: UserProfileService = Depends()
):
    return await user_profile_service.write_to_profile(user_profile, photo, Authorization)


@user_profile_router.get('/', response_model=UserProfileOut)
async def get_profile(
    Authorization: str = Header(None),
    user_profile_service: UserProfileService = Depends()
):
    return await user_profile_service.get_profile(Authorization)
