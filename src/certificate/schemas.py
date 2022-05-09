from uuid import UUID

from pydantic import Field
from pydantic.main import BaseModel

from src.discipline.types import Disciplines


class CertificateOut(BaseModel):
    id: UUID
    fullname: str = Field(alias="fullName")
    filename: str = Field(alias="testName")
    score: int
    date: str = Field(alias="passDate")
    discipline: Disciplines

