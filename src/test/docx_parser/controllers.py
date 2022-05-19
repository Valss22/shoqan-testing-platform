from fastapi import APIRouter, Depends, Header
from starlette.background import BackgroundTasks

from src.test.docx_parser.schemas import PassTestIn, PassTestOut
from src.test.docx_parser.service import ParserService

parser_router = APIRouter(
    prefix="/test/{test_id}"
)


@parser_router.get("/")
async def get_parsed_docx(
    test_id: str,
    parser_service: ParserService = Depends()
):
    return await parser_service.get_parsed_docx(test_id)


@parser_router.post("/", response_model=PassTestOut)
async def pass_test(
    test_id: str,
    answers: PassTestIn,
    background_tasks: BackgroundTasks,
    Authorization: str = Header(...),
    parser_service: ParserService = Depends()
):
    return await parser_service.get_points(
        test_id, Authorization,
        answers, background_tasks
    )
