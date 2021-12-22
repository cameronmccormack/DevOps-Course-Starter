import urllib.parse
import requests

from todo_app.trello_config import Config
from todo_app.models.status import Status


class TrelloRepository:
    def __init__(self):
        self.config = Config()
        self.auth_query_params = {
            "key": self.config.TRELLO_API_KEY,
            "token": self.config.TRELLO_TOKEN
        }

    def fetch_lists(self):
        url = self.build_trello_url(
            f"boards/{self.config.BOARD_ID}/lists",
            {"cards": "open"}
        )
        return requests.get(url).json()

    def create_card(self, name):
        url = self.build_trello_url(
            "cards",
            {"name": name, "idList": self.config.NOT_STARTED_LIST_ID}
        )
        requests.post(url)

    def delete_card(self, id):
        url = self.build_trello_url(f"cards/{id}")
        requests.delete(url)

    def update_status(self, id, status):
        url = self.build_trello_url(
            f"cards/{id}",
            {"idList": self.get_list_id_for_status(status)}
        )
        requests.put(url)

    def build_trello_url(self, path, extra_query_params={}):
        query_params = self.auth_query_params | extra_query_params
        return f"{self.config.BASE_URL}{path}?{urllib.parse.urlencode(query_params)}"

    def get_list_id_for_status(self, status):
        if status == Status.NOT_STARTED:
            return self.config.NOT_STARTED_LIST_ID
        elif status == Status.IN_PROGRESS:
            return self.config.IN_PROGRESS_LIST_ID
        else:
            return self.config.DONE_LIST_ID
