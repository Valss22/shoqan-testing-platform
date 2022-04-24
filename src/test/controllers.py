from fastapi import APIRouter, UploadFile, Body, Depends, Header, File

from src.discipline.types import Disciplines
from src.test.schemas import TestOut
from src.test.service import TestService

test_router = APIRouter(
    prefix="/test"
)


@test_router.post("/")
async def create_test(
    info: UploadFile = Body(...),
    file: UploadFile = File(...),
    test_service: TestService = Depends()
):
    return await test_service.create_test(info, file)


@test_router.get("/", response_model=list[TestOut])
async def get_tests(
    discipline: Disciplines,
    test_service: TestService = Depends()
):
    return await test_service.get_tests(discipline)
