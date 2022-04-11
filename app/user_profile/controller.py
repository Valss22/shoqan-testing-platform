from fastapi import APIRouter

from app.user_profile.model import UserProfile
from app.user_profile.schemas import UserProfileIn

user_profile_router = APIRouter(
    prefix='/user/profile'
)


# @user_profile_router.post('/')
# async def write_to_user_profile(user_profile: UserProfileIn):
#     return await UserProfile.create(**user_profile.dict())
