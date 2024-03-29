import json
from typing import Union, Final

from fastapi import UploadFile
import cloudinary.uploader as cloud
from tortoise.exceptions import DoesNotExist

from src.competence.model import Competence
from src.competence.types import Competencies
from src.discipline.model import Discipline
from src.discipline.types import Disciplines
from src.middlewares.auth import get_current_user_id
from src.test.model import Test, UserToTest
from src.test.types import InfoKeys
from src.user.model import User
import datetime

SCORE_THRESHOLD: Final[int] = 15


class TestService:
    async def create_test(self, info: UploadFile, file: UploadFile):
        filename = file.filename.split(".docx")[0]
        uploaded_file = cloud.upload(file.file, resource_type="auto")
        info_str: str = info.file.__dict__["_file"].read().decode("utf-8")
        info_obj: dict[
            InfoKeys,
            Union[Discipline, list[Competencies]]
        ] = json.loads(info_str)

        discipline, need_to_create = await Discipline.get_or_create(
            name=info_obj[InfoKeys.DISCIPLINE.value]
        )
        if need_to_create:
            await discipline.save()
        test = await Test.create(
            file=uploaded_file["secure_url"],
            filename=filename,
            discipline=discipline
        )
        await test.save()
        competencies: list[Competencies] = info_obj[InfoKeys.COMPETENCIES.value]
        for comp in competencies:
            competence, need_to_create = await \
                Competence.get_or_create(name=comp)
            await competence.disciplinies.add(discipline)
            if need_to_create:
                await competence.save()
            await test.competencies.add(competence)

    async def get_tests(self, discipline: Disciplines, auth_header: str):
        tests: list[Test] = await Test.filter(
            discipline__name=discipline
        )
        user_id = get_current_user_id(auth_header)

        response: list[dict] = []

        i = 0
        for test in tests:
            try:
                user_test: UserToTest = await UserToTest.get(
                    user_id=user_id,
                    test_id=test.id
                )
                response.append({
                    "passed": user_test.passed,
                    "attempts": user_test.attempts
                })
            except DoesNotExist:
                response.append({
                    "passed": None,
                    "attempts": 0,
                })
            response[i].update(test.__dict__)
            i += 1

        return response

    async def write_result(self, test_id: str, user_id: str, score: int) -> None:
        try:
            user_test: UserToTest = await UserToTest.get(
                user_id=user_id,
                test_id=test_id
            )
        except DoesNotExist:
            user = await User.get(id=user_id)
            test = await Test.get(id=test_id)
            user_test: UserToTest = await UserToTest.create(
                user=user, test=test
            )

        if score >= SCORE_THRESHOLD:
            user_test.passed = True
            user_test.date = str(datetime.date.today())
        else:
            user_test.attempts += 1
            if user_test.attempts == 3:
                user_test.passed = False
        user_test.score = score
        await user_test.save(
            update_fields=["score", "passed", "attempts", "date"]
        )

