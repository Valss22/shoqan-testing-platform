from app.user.model import User
from app.user.schemas import UserIn
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.starttls()

smtp.login('valsshokorov@gmail.com', os.getenv('EMAIL_PASSWORD'))

smtp.sendmail('valsshokorov@gmail.com', ['deger.begerrr@gmail.com'], 'password123')
smtp.quit()


class UserService:
    async def create_user(self, user: UserIn):
        await User.create(**user.dict(), password_hash='fsdf')
        return await User.get(email=user.dict()['email'])

    def generate_password(self):
        return '123'

    def send_password_to_email(self):
        pass
