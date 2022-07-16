import smtplib
from email.message import EmailMessage
from time import sleep
from typing import Final, Union

import pdfkit
from docx import Document
from pydantic.networks import EmailStr
from src.static.emails import admin_emails

ROOT_EMAIL: Final[str] = "ShoqanPlatform@gmail.com"
# ROOT_PASSWORD: Final[str] = "mLq-8eS-NAA-S9T" Пароль от почты#
ROOT_PASSWORD: Final[str] = "zwqpxcekrenbpify"  # Пароль для входа с third party app


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

    def send_certificate(
        self, email: EmailStr, score: int,
        test_name: str, discipline: str
    ) -> None:
        content: str = f"Вы успешно прошли тестирование" \
                       f" '{test_name}' по дисциплине" \
                       f" '{discipline}'\n" \
                       f"Количество балов - {score} / 30"
        self.send_email(content, email, "Сертификат")

    def send_certificate_to_admin(
        self, email: EmailStr,
        score: int, test_name: str, discipline: str
    ) -> None:
        content: str = f"Студент {email} успешно прошел тестирование" \
                       f" '{test_name}'\n" \
                       f"По дисциплине '{discipline}'\n" \
                       f"Количество балов - {score} / 30"
        self.send_email(content, admin_emails[1], "Сертификат студента")

    def __del__(self):
        self.smtp.quit()


# email_sender_service = EmailSenderService()


# def send_pdf():
#     document = Document("../static/certificate.docx")
#     for paragraph in document.paragraphs:
#         paragraph.text = paragraph.text.replace("{test}", "Тест1")
#         paragraph.text = paragraph.text.replace("{fullname}", "ФИО1")
#         paragraph.text = paragraph.text.replace("{score}", "20")
#         paragraph.text = paragraph.text.replace("{date}", "2020-16-7")
#
#     document.save("../static/certificate.pdf")
#
#
# send_pdf()

from jinja2 import Environment, FileSystemLoader

name = 'Александр'

config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
env = Environment(loader=FileSystemLoader('.'))

template = env.get_template("certificate.html")

pdf_template = template.render({'name': name})

pdfkit.from_string(pdf_template, 'out.pdf', configuration=config)
