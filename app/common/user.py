from typing import Optional

import jwt

from app.settings import TOKEN_KEY


def get_current_user_id(auth_header: str) -> Optional[str]:
    if auth_header:
        decoded_token: dict = jwt.decode(
            auth_header, TOKEN_KEY, algorithms='HS256'
        )
        return str(decoded_token['id'])
    raise ValueError
