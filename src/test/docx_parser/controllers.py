from fastapi import APIRouter, Depends

from src.test.docx_parser.service import ParserService

parser_router = APIRouter(
    prefix="/test"
)


@parser_router.get("/{test_id}")
async def get_parsed_docx(
    test_id: str,
    parser_service: ParserService = Depends()
):
    return await parser_service.parse_docx(test_id)
