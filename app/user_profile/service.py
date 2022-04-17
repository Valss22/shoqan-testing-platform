import json

import cloudinary.uploader
from fastapi import UploadFile

from app.common.user import get_current_user_id
from app.user.model import User
from app.user_profile.model import UserProfile


class UserProfileService:

    # async def write_to_user_profile(self, **kwargs):
    #     photo: UploadFile = kwargs["photo"]
    #     uploaded_photo = cloudinary.uploader.upload(photo.file, resource_type="auto")
    #
    #     current_user_id = get_current_user_id(kwargs["auth_header"])
    #
    #     user_profile = await UserProfile.create(
    #         fullname=kwargs["fullname"],
    #         specialty=kwargs["specialty"],
    #         course=kwargs["course"],
    #         photo=uploaded_photo["secure_url"]
    #     )
    #     await user_profile.save()
    #     await User.get(id=current_user_id)\
    #         .update(user_profile=user_profile)
    #     return user_profile

    async def write_to_user_profile(self, user_profile, photo, auth_header):
        user_profile = json.loads(user_profile)

        uploaded_photo = cloudinary.uploader.upload(photo.file, resource_type="auto")
        current_user_id = get_current_user_id(auth_header)
        user_profile = await UserProfile.create(**user_profile, photo=uploaded_photo["secure_url"])

        await user_profile.save()
        await User.get(id=current_user_id) \
            .update(user_profile=user_profile)

        return user_profile
