from typing import Final
from random import shuffle
from docx import Document
import re


from src.test.model import Test

NUMBER_QUESTIONS: Final[int] = 30
NUMBER_ANSWERS: Final[int] = 5

QUESTION_TAG: Final[str] = "<question>"
ANSWER_TAG: Final[str] = "<variant>"


class ParserService:

    async def parse_docx(self, test_id: str):
        questions = []
        answers = []
        docx_response: list[dict] = []

        #docx_file = await Test.get(id=test_id).only("file")
        docx_file = "https://res.cloudinary.com/dmh0ekjaw/raw/upload/v1651494632/scywbbwswdrujg1ktynu"


        document = Document(docx_file)
        blocks: list[str] = [block.text for block in document.paragraphs]

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
