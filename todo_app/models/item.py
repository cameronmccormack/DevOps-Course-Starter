from todo_app.models.status import Status


class Item:
    def __init__(self, id, name, status=Status.NOT_STARTED):
        self.id = id
        self.name = name
        self.status = status

    @classmethod
    def from_trello_card(cls, card, status):
        return cls(card["id"], card["name"], status)
