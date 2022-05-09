from pydantic import BaseModel

from src.competence.types import Competencies


class CompetenceOut(BaseModel):
    competencies: list[Competencies]
