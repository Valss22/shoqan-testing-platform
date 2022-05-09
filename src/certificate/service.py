from starlette.responses import JSONResponse

from src.middlewares.auth import get_current_user_id
from src.test.model import Test, UserToTest
from src.user.model import User


class CertificateService:

    async def get_all_certificates(self, all_users: bool, auth_header: str):

        if all_users:
            tests = await Test.filter(
                user_to_tests__passed=True,
            ).prefetch_related("users") \
                .prefetch_related("discipline")
            user_tests = await UserToTest.filter(passed=True)
        else:
            user_id = get_current_user_id(auth_header)
            user = await User.get(id=user_id) \
                .only("user_profile_id") \
                .prefetch_related("user_profile")
            fullname = user.user_profile.fullname
            tests = await Test.filter(
                user_to_tests__passed=True,
                user_to_tests__user_id=user_id
            ).prefetch_related("users") \
                .prefetch_related("discipline")
            user_tests = await UserToTest.filter(
                user_id=user_id, passed=True
            )

        response = []
        for i in range(len(tests)):
            if all_users:
                user_id = user_tests[i].user_id
                user = await User.get(id=user_id).prefetch_related("user_profile")
                fullname = user.user_profile.fullname
            response.append({
                "id": tests[i].id,
                "fullName": fullname,
                "testName": tests[i].filename,
                "score": user_tests[i].score,
                "passDate": user_tests[i].date,
                "discipline": tests[i].discipline.name
            })

            return response
