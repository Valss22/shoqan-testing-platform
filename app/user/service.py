from pydantic import EmailStr

from app.user.model import User
from app.user.schemas import UserIn
import smtplib
import secrets


class UserService:
    async def create_user(self, user: UserIn) -> None:
        password: str = secrets.token_urlsafe(32)
        email: EmailStr = user.dict()['email']
        self.send_password_to_email(password, email)
        await User.create(**user.dict(), password_hash=password)

    def send_password_to_email(self, password: str, email: EmailStr) -> None:
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login('ShoqanPlatform@gmail.com', 'mLq-8eS-NAA-S9T')
        smtp.sendmail('ShoqanPlatform@gmail.com', [email], password)
        smtp.quit()
