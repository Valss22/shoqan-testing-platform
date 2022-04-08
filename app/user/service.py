from app.user.model import User
from app.user.schemas import UserIn
import smtplib
import os
from dotenv import load_dotenv
import secrets

load_dotenv()


# TODO: Валидация для email
class UserService:
    async def create_user(self, user: UserIn) -> None:
        password: str = secrets.token_urlsafe(32)
        email: str = user.dict()['email']
        self.send_password_to_email(password, email)
        await User.create(**user.dict(), password_hash=password)

    def send_password_to_email(self, password: str, email: str) -> None:
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login('valsshokorov@gmail.com', os.getenv('EMAIL_PASSWORD'))
        smtp.sendmail('valsshokorov@gmail.com', [email], password)
        smtp.quit()
