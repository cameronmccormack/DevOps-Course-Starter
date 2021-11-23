import urllib.parse
import requests

from todo_app.trello_config import Config

from todo_app.models.item import Item
from todo_app.models.status import Status

config = Config()
auth_query_params = {
    "key": config.TRELLO_API_KEY,
    "token": config.TRELLO_TOKEN
}


def fetch_cards():
    url = build_trello_url(
        f"boards/{config.BOARD_ID}/lists",
        {"cards": "open"}
    )
    response = requests.get(url).json()
    not_started_cards = map_cards_for_status(response, Status.NOT_STARTED)
    in_progress_cards = map_cards_for_status(response, Status.IN_PROGRESS)
    done_cards = map_cards_for_status(response, Status.DONE)
    return not_started_cards + in_progress_cards + done_cards


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


def map_cards_for_status(response, status):
    list_id = get_list_id_for_status(status)
    trello_cards = next(
        list for list in response if list["id"] == list_id
    )["cards"]
    return [Item.from_trello_card(card, status) for card in trello_cards]


def get_list_id_for_status(status):
    if status == Status.NOT_STARTED:
        return config.NOT_STARTED_LIST_ID
    elif status == Status.IN_PROGRESS:
        return config.IN_PROGRESS_LIST_ID
    else:
        return config.DONE_LIST_ID
