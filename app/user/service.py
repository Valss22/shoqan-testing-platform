from time import time
from typing import Optional, Union
from uuid import UUID

import bcrypt
import jwt
from pydantic import EmailStr
from starlette import status
from starlette.responses import JSONResponse

from app.settings import TOKEN_KEY, TOKEN_TIME
from app.user.model import User
from app.user.schemas import UserIn, UserOut
import smtplib
import secrets


class UserService:
    async def create_user(self, user: UserIn) -> None:
        password: Optional[str, bytes] = secrets.token_urlsafe(4)
        email: EmailStr = user.dict()['email']
        self.send_password_to_email(password, email)
        password = password.encode()
        await User.create(**user.dict(), password_hash=password)

    def send_password_to_email(self, password: str, email: EmailStr) -> None:
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login('ShoqanPlatform@gmail.com', 'mLq-8eS-NAA-S9T')
        smtp.sendmail('ShoqanPlatform@gmail.com', [email], password)
        smtp.quit()

    async def auth_user(self, user: UserIn, is_admin: bool) -> Union[None, dict, JSONResponse]:
        email: EmailStr = user.dict()['email']
        password: bytes = user.dict()['password'].encode()
        user_obj = await User.get(email=email)

        if bcrypt.checkpw(password, user_obj.password_hash):
            payload: dict = {
                'id': str(user_obj.id),
                'email': user_obj.email,
                'isAdmin': is_admin,
                'exp': time() + TOKEN_TIME
            }
            return {
                **user_obj.__dict__,
                'token': jwt.encode(payload, TOKEN_KEY),
                'isAdmin': is_admin
            }
        return JSONResponse(
            {'msg': 'wrong password'},
            status.HTTP_400_BAD_REQUEST
        )


