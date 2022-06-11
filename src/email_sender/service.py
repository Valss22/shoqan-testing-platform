import smtplib
from email.message import EmailMessage
from time import sleep
from typing import Final, Union
from pydantic.networks import EmailStr

from src.discipline.types import Disciplines
from src.static.emails import admin_emails

ROOT_EMAIL: Final[str] = "ShoqanPlatform@gmail.com"
# ROOT_PASSWORD: Final[str] = "mLq-8eS-NAA-S9T"
ROOT_PASSWORD: Final[str] = "zwqpxcekrenbpify"


class EmailSenderService:
    def __init__(self):
        self.smtp = smtplib.SMTP("smtp.gmail.com", 587)
        self.smtp.starttls()
        self.smtp.login(ROOT_EMAIL, ROOT_PASSWORD)
        self.msg = EmailMessage()
        self.msg["From"] = ROOT_EMAIL

    def send_email(
        self, content: str,
        reciever: Union[list[str], str],
        subject: str
    ) -> None:
        sleep(5)
        del self.msg["To"]
        del self.msg["Subject"]
        self.msg.set_content(
            content, subtype="plain",
            charset="utf-8"
        )
        self.msg["To"] = reciever
        self.msg["Subject"] = subject
        self.smtp.send_message(self.msg)

    def send_password(self, password: str, email: EmailStr) -> None:
        content: str = f"Ваш пароль для входа в систему: {password}"
        self.send_email(content, email, "Подтверждение пароля")

    def send_certificate(
        self, email: EmailStr, score: int,
        test_name: str, discipline: Disciplines
    ) -> None:
        content: str = f"Вы успешно прошли тестирование" \
                       f" '{test_name}' по дисциплине" \
                       f" '{discipline.value}'\n" \
                       f"Количество балов - {score} / 30"
        self.send_email(content, email, "Сертификат")

    def send_certificate_to_admin(
        self, email: EmailStr,
        score: int, test_name: str, discipline: Disciplines
    ) -> None:
        content: str = f"Студент {email} успешно прошел тестирование" \
                       f" '{test_name}'\n" \
                       f"По дисциплине '{discipline.value}'\n" \
                       f"Количество балов - {score} / 30"
        self.send_email(content, admin_emails[1], "Сертификат студента")

    def __del__(self):
        self.smtp.quit()


email_sender_service = EmailSenderService()
