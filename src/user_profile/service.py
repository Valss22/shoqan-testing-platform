import cloudinary.uploader as cloud
from fastapi import UploadFile
from src.middlewares.auth import get_current_user, get_current_user_id
from src.user.model import User
from src.user_profile.model import UserProfile
import json


class UserProfileService:
    async def write_to_profile(
        self, user_profile: UploadFile,
        photo: UploadFile, auth_header: str
    ):
        uploaded_photo = cloud.upload(photo.file, resource_type="auto")

        current_user: User = await get_current_user(auth_header)
        user_profile_str = user_profile.file.__dict__["_file"].read().decode("utf-8")
        user_profile_obj = await UserProfile.create(
            **json.loads(user_profile_str),
            photo=uploaded_photo["secure_url"]
        )
        await user_profile_obj.save()
        current_user.user_profile = user_profile_obj
        await current_user.save(update_fields=["user_profile_id"])
        return user_profile_obj

    async def get_profile(self, auth_header: str):
        current_user_id = get_current_user_id(auth_header)
        user_obj = await User.get(
            id=current_user_id
        ).prefetch_related("user_profile")
        profile = user_obj._user_profile
        if profile:
            profile = profile.__dict__
        return profile
 