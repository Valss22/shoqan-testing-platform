import json
from typing import Union

from fastapi import UploadFile
import cloudinary.uploader as cloud
from src.competence.model import Competence
from src.competence.types import Competencies
from src.discipline.model import Discipline
from src.discipline.types import Disciplines
from src.middlewares.auth import get_current_user_id
from src.test.model import Test
from src.test.types import InfoKeys


class TestService:
    async def create_test(self, info: UploadFile, file: UploadFile):
        filename = file.filename.split(".docx")[0]

        uploaded_file = cloud.upload(file.file, resource_type="auto")

        info_str: str = info.file.__dict__["_file"].read().decode("utf-8")

        info_obj: dict[
            InfoKeys,
            Union[Discipline, list[Competencies]]
        ] = json.loads(info_str)

        # info_obj = {
        #     "discipline": "Безопасность данных",
        #     "competencies": [
        #         "Проектные документы",
        #         "Технические задания"]
        # }

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
            competence, need_to_create = await Competence.get_or_create(name=comp)
            await competence.disciplinies.add(discipline)
            if need_to_create:
                await competence.save()
            await test.competencies.add(competence)

    async def get_tests(self, discipline: Disciplines, auth_header):
        tests: list[Test] = await Test.filter(discipline__name=discipline)
        # user_id = get_current_user_id(auth_header)

        # response = []

        for test in tests:
            await test.fetch_related("users")

            # if user_id in test.users:
            #     response.append({**test, "passed": True})
            # else:
            #     response.append({**test, "passed": False})

        return tests
