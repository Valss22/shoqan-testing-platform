import smtplib
from typing import Final

from pydantic.networks import EmailStr

ROOT_EMAIL: Final[str] = "ShoqanPlatform@gmail.com"
ROOT_PASSWORD: Final[str] = "mLq-8eS-NAA-S9T"


class EmailSenderService:
    def __init__(self):
        self.smtp = smtplib.SMTP("smtp.gmail.com", 587)
        self.smtp.starttls()
        self.smtp.login(ROOT_EMAIL, ROOT_PASSWORD)

    def send_password(self, password: str, email: EmailStr) -> None:
        self.smtp.sendmail(ROOT_EMAIL, [email], password)
        self.smtp.quit()

    def send_certificate(
        self, email: EmailStr, score: int,
        test_name: str, discipline: str
    ) -> None:
        # message: str = f"Вы успешно прошли тестирование" \
        #                f" '{test_name}' по дисциплине" \
        #                f" '{discipline}'. Количество балов - {score} / 30"

        message: str = f"{score} / 30"
        self.smtp.sendmail(ROOT_EMAIL, [email], message)
