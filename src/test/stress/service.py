from typing import Optional

from starlette.responses import JSONResponse

from src.middlewares.auth import get_current_user, get_current_user_id
from src.static.psychology import stress_obj
from src.user.model import User
from src.user_profile.model import UserProfile


class StressService:
    async def get_stress_result(self, auth_header: str):

        # current_user_id = get_current_user_id(auth_header)

        current_user: User = await get_current_user(auth_header)

        user_profile: Optional[UserProfile] = await current_user.fetch_related("user_profile")

        if user_profile:
            if user_profile.stress:
                return JSONResponse({"passed": True, "test": stress_obj})
            return JSONResponse({"passed": False, "test": None})
        raise Exception  # TODO: сделать искл. и мидл
