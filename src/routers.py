from fastapi import APIRouter

from src.test.controllers import test_router
from src.test.stress.controllers import stress_router
from src.user.controllers import user_router
from src.user_profile.controllers import user_profile_router

api_router = APIRouter()
api_router.include_router(user_router)
api_router.include_router(user_profile_router)
api_router.include_router(test_router)
api_router.include_router(stress_router)
