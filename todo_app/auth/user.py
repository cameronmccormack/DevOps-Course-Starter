from flask_login import UserMixin

from todo_app.auth.user_roles import UserRoles

WRITER_IDS = ["39823505"]


class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.role = UserRoles.WRITER if id in WRITER_IDS else UserRoles.READER
