from smtplib import SMTPException
from typing import Final
from random import shuffle

from docx import Document
import re
import shutil
import requests
from pydantic.networks import EmailStr

from src.email_sender.service import email_sender_service
from src.middlewares.auth import get_current_user_id
from src.test.docx_parser.schemas import PassTestIn
from src.test.model import Test
from src.test.service import TestService, SCORE_THRESHOLD
from src.user.model import User

NUMBER_QUESTIONS: Final[int] = 30
NUMBER_ANSWERS: Final[int] = 5

QUESTION_TAG: Final[str] = "<question>"
ANSWER_TAG: Final[str] = "<variant>"


class ParserService:
    def __init__(self):
        self.test_service = TestService()
        self.email_sender_service = email_sender_service  # TODO: Возможно добавить IoC

    async def read_docx(self, test_id: str) -> list[str]:
        docx_url = await Test.get(id=test_id).only("file")
        docx_url = docx_url.file

        docx_url_response = requests.get(docx_url, stream=True)
        with open("src/static/test.docx", "wb") as out_file:
            shutil.copyfileobj(docx_url_response.raw, out_file)
        del docx_url_response

        document = Document("src/static/test.docx")
        blocks: list[str] = [block.text for block in document.paragraphs]
        return blocks

    async def get_parsed_docx(self, test_id: str):
        questions = []
        answers = []
        docx_response: list[dict] = []
        blocks: list[str] = await self.read_docx(test_id)
        for i in blocks:
            if QUESTION_TAG in i:
                questions.append(i.split(QUESTION_TAG)[1].strip())
            elif ANSWER_TAG in i:
                answer = i.split(ANSWER_TAG)[1].strip()
                answer = re.sub(r"\t", " ", answer)
                answers.append(answer)
        i = 0
        for q in questions:
            a = answers[i:i + NUMBER_ANSWERS]
            shuffle(a)
            docx_block: dict = {
                "question": q,
                "answers": a
            }
            docx_response.append(docx_block)
            i += NUMBER_ANSWERS
        return docx_response

    async def get_points(self, test_id: str, auth_header: str, answers: PassTestIn):
        user_id = get_current_user_id(auth_header)
        answers: list[str] = answers.dict()["answers"]
        score: int = 0
        blocks: list[str] = await self.read_docx(test_id)
        n_q = -1
        n_a = 0
        for i in blocks:
            if ANSWER_TAG in i:
                if n_a % 5 == 0 or n_a == 0:
                    answer = i.split(ANSWER_TAG)[1].strip()
                    answer = re.sub(r"\t", " ", answer)
                    if answer == answers[n_q]:
                        score += 1
                n_a += 1
            elif QUESTION_TAG in i:
                n_q += 1
        await self.test_service.write_result(test_id, user_id, score)

        if score >= SCORE_THRESHOLD:
            passed = True
            test = await Test.get(id=test_id).only(
                "filename", "discipline_id"
            ).prefetch_related("discipline")

            user = await User.get(id=user_id).only("email")
            email: EmailStr = user.email

            test_name: str = test.filename
            discipline: str = test.discipline.name
            try:
                self.email_sender_service.send_certificate(
                    email, score, test_name, discipline
                )
                self.email_sender_service.send_certificate_to_admins(
                    email, score, test_name, discipline
                )
            except SMTPException:
                pass
        else:
            passed = False

        return {
            "score": score,
            "passed": passed
        }
