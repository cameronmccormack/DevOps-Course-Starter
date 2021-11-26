import urllib.parse
import requests

from todo_app.trello_config import Config
from todo_app.models.status import Status

config = Config()
auth_query_params = {
    "key": config.TRELLO_API_KEY,
    "token": config.TRELLO_TOKEN
}


def fetch_lists():
    url = build_trello_url(
        f"boards/{config.BOARD_ID}/lists",
        {"cards": "open"}
    )
    return requests.get(url).json()


def create_card(name):
    url = build_trello_url(
        "cards",
        {"name": name, "idList": config.NOT_STARTED_LIST_ID}
    )
    requests.post(url)


def delete_card(id):
    url = build_trello_url(f"cards/{id}")
    requests.delete(url)


def update_status(id, status):
    url = build_trello_url(
        f"cards/{id}",
        {"idList": get_list_id_for_status(status)}
    )
    requests.put(url)


def build_trello_url(path, extra_query_params={}):
    query_params = auth_query_params | extra_query_params
    return f"{config.BASE_URL}{path}?{urllib.parse.urlencode(query_params)}"


def get_list_id_for_status(status):
    if status == Status.NOT_STARTED:
        return config.NOT_STARTED_LIST_ID
    elif status == Status.IN_PROGRESS:
        return config.IN_PROGRESS_LIST_ID
    else:
        return config.DONE_LIST_ID
