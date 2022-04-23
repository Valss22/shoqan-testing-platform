from fastapi import Depends, Header, APIRouter
from src.test.stress.schemas import StressOut, StressIn
from src.test.stress.service import StressService

stress_router = APIRouter(
    prefix="/test/stress"
)


@stress_router.get("/", response_model=StressOut)
async def get_stress_result(
    Authorization: str = Header(...),
    stress_service: StressService = Depends()
):
    return await stress_service.get_stress_result(Authorization)


@stress_router.post("/")
async def write_stress_result(
    stress: StressIn,
    Authorization: str = Header(...),
    stress_service: StressService = Depends()
):
    return await stress_service.write_stress_result(stress, Authorization)
