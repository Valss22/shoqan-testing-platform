import json

import cloudinary.uploader
from fastapi import UploadFile
from starlette import status
from starlette.responses import JSONResponse

from app.common.user import get_current_user_id
from app.user.model import User
from app.user_profile.model import UserProfile
import json


class UserProfileService:
    async def write_to_profile(self, user_profile: UploadFile, photo, auth_header):
        uploaded_photo = cloudinary.uploader.upload(photo.file, resource_type="auto")
        current_user_id = get_current_user_id(auth_header)
        user_obj = User.get(id=current_user_id)

        if user_obj:
            user_profile = user_profile.file.__dict__["_file"].read().decode("utf-8")
            user_profile = await UserProfile.create(
                **json.loads(user_profile),
                photo=uploaded_photo["secure_url"]
            )
            await user_profile.save()
            await user_obj.update(user_profile=user_profile)
            return user_profile

        return JSONResponse(
            {"msg": "user doesnt exist"},
            status.HTTP_400_BAD_REQUEST
        )

    async def get_profile(self, auth_header: str):
        current_user_id = get_current_user_id(auth_header)

        user_obj = await User.get(
            id=current_user_id
        ).prefetch_related("user_profile")

        profile = user_obj._user_profile
        if profile:
            profile = profile.__dict__

        return profile
