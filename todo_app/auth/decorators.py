from functools import wraps
from flask_login import current_user

from todo_app.auth.user_roles import UserRoles


def requireWriter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_anonymous or current_user.role == UserRoles.WRITER:
            return func(*args, **kwargs)
        else:
            return {"message": "Unauthorized"}, 401
    return wrapper
