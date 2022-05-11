from src.middlewares.auth import get_current_user_id
from src.test.model import Test


class CompetenceService:

    async def get_competencies(self, auth_header: str):
        user_id = get_current_user_id(auth_header)
        tests = await Test.filter(
            user_to_tests__user_id=user_id,
            user_to_tests__passed=True,
        ).prefetch_related("competencies")

        competencies: list[str] = []
        for test in tests:
            for comp in test.competencies.related_objects:
                if comp.name.value not in competencies:
                    competencies.append(comp.name.value)
        return {
            "competencies": competencies
        }
