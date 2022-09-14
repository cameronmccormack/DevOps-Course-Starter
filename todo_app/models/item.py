from todo_app.models.status import Status


class Item:
    def __init__(
        self,
        id,
        name,
        last_status_change_datetime,
        status=Status.NOT_STARTED
    ):
        self.id = id
        self.name = name
        self.last_status_change_datetime = last_status_change_datetime
        self.status = status

    @classmethod
    def from_mongo_db_item(cls, card):
        return cls(
            card["_id"],
            card["name"],
            card["last_status_change_datetime"],
            card["status"]
        )
