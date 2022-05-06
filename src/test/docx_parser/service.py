from typing import Final
from random import shuffle

from docx import Document
import re
import shutil
import requests

from src.test.docx_parser.schemas import PassTestIn
from src.test.model import Test
from src.test.service import TestService, SCORE_THRESHOLD

NUMBER_QUESTIONS: Final[int] = 30
NUMBER_ANSWERS: Final[int] = 5

QUESTION_TAG: Final[str] = "<question>"
ANSWER_TAG: Final[str] = "<variant>"


class ParserService:
    def __init__(self):
        self.test_service = TestService()

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
            i += 1
        return docx_response

    async def get_points(self, test_id: str, auth_header: str, answers: PassTestIn):
        answers: list[str] = answers.dict()["answers"]
        score = 0
        blocks: list[str] = await self.read_docx(test_id)
        n = 0
        for i in blocks:
            if ANSWER_TAG in i:
                answer = i.split(ANSWER_TAG)[1].strip()
                answer = re.sub(r"\t", " ", answer)
                if answer == answers[n]:
                    score += 1
            n += 1
        await self.test_service.write_result(test_id, auth_header, score)

        return {
            "score": score,
            "passed": True if score >= SCORE_THRESHOLD else False
        }
