from functools import wraps

from app.admin.emails import admin_emails


def is_admin(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        admin_email = kwargs['user_in'].dict()['email']
        admin_bool: bool = admin_email in admin_emails
        return await kwargs['user_service'].auth_user(kwargs['user_in'], admin_bool)

    return wrapper
