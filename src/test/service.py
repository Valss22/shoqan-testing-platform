import json

from fastapi import UploadFile
import cloudinary.uploader as cloud

from src.competence.model import Competence
from src.competence.types import Competencies
from src.discipline.model import Discipline
from src.middlewares.auth import get_current_user_id
from src.test.model import Test
from src.user.model import User


class TestService:
    async def create_test(self, info: UploadFile, file: UploadFile):

        uploaded_file = cloud.upload(file.file, resource_type="auto")
        info_str: str = info.file.__dict__["_file"].read().decode("utf-8")
        info_obj: dict = json.loads(info_str)
        # info_obj = {"discipline": "Безопасность данных",
        #             "competencies": ["Проектные документы","Технические задания"]}

        discipline, need_to_create = await Discipline.get_or_create(name=info_obj["discipline"])
        if need_to_create:
            await discipline.save()

        test = await Test.create(
            file=uploaded_file["secure_url"],
            discipline=discipline
        )
        await test.save()

        competencies: list[Competencies] = info_obj["competencies"]

        for comp in competencies:
            competence, need_to_create = await Competence.get_or_create(name=comp)

            await competence.disciplinies.add(discipline)
            await test.competencies.add(competence)

            if need_to_create:
                await competence.save()
