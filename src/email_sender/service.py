from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
from email.message import EmailMessage
from time import sleep
from typing import Final, Union
from jinja2 import Environment, FileSystemLoader
import pdfkit
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

        self.msg_for_pdf = MIMEMultipart()

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
        self, fullname, email: EmailStr, score: int,
        test_name: str, discipline: str
    ) -> None:
        config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template("certificate.html")
        pdf_template = template.render({
            "fullname": fullname,
            "test": test_name,
            "discipline": discipline,
            "score": str(score)
        })
        pdfkit.from_string(pdf_template, 'out.pdf', configuration=config)

        with open("out.pdf", "rb") as f:
            attach = MIMEApplication(f.read(), _subtype="pdf")
        self.msg_for_pdf.attach(attach)
        attach.add_header('Content-Disposition', 'attachment', filename=f"Сертификат {discipline}")
        self.msg_for_pdf.attach(attach)
        self.msg_for_pdf["To"] = email
        self.msg_for_pdf["Subject"] = "Сертификат о прохождении тестирования"
        self.smtp.send_message(self.msg_for_pdf)

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


email_sender_service = EmailSenderService()

# def send_pdf(reciever: str):
#     config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
#     env = Environment(loader=FileSystemLoader('.'))
#     template = env.get_template("certificate.html")
#     pdf_template = template.render({'fullname': name})
#     pdfkit.from_string(pdf_template, 'out.pdf', configuration=config, options={"page-size": "A3"})
#
#     smtp = smtplib.SMTP("smtp.gmail.com", 587)
#     smtp.starttls()
#     smtp.login(ROOT_EMAIL, ROOT_PASSWORD)
#     msg = MIMEMultipart()
#     msg["From"] = ROOT_EMAIL
#
#     with open("out.pdf", "rb") as f:
#         attach = MIMEApplication(f.read(), _subtype="pdf")
#
#     attach.add_header('Content-Disposition', 'attachment', filename=str("open.pdf"))
#     msg.attach(attach)
#
#     msg["To"] = reciever
#     msg["Subject"] = "Сертификат о прохождении тестирования"
#     smtp.send_message(msg)
