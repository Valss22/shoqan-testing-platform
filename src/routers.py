from fastapi import APIRouter

from src.user.controllers import user_router
from src.user_profile.controller import user_profile_router

api_router = APIRouter()
api_router.include_router(user_router)
api_router.include_router(user_profile_router)