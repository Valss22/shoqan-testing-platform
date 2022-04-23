from fastapi import Depends, Header, APIRouter
from src.test.controllers import test_router
from src.test.stress.schemas import StressOut
from src.test.stress.service import StressService

stress_router = APIRouter(
    prefix="/test"
)


@stress_router.get("/stress")
async def get_stress_result(
    Authorization: str = Header(...),
    stress_service: StressService = Depends()
):
    return await stress_service.get_stress_result(Authorization)
