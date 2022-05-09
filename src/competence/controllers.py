from fastapi import APIRouter, Header, Depends

from src.competence.schemas import CompetenceOut
from src.competence.service import CompetenceService

competence_router = APIRouter(
    prefix="/competence"
)


@competence_router.get("/", response_model=CompetenceOut)
async def get_competencies(
    Authorization: str = Header(...),
    competence_service: CompetenceService = Depends()
):
    return await competence_service.get_competencies(Authorization)
