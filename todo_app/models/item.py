from todo_app.models.status import Status
from dateutil.parser import isoparse


class Item:
    def __init__(
        self,
        id,
        name,
        last_modified_datetime_string,
        status=Status.NOT_STARTED
    ):
        self.id = id
        self.name = name
        self.status = status
        self.last_status_change_datetime = isoparse(
            last_modified_datetime_string
        )

    @classmethod
    def from_trello_card(cls, card, status):
        return cls(card["id"], card["name"], card["dateLastActivity"], status)
