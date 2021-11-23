from todo_app.repository import trello_repository
from todo_app.models.status import Status
from todo_app.models.item import Item


def get_items():
    """
    Fetches all saved items from Trello.

    Returns:
        list: The list of saved items.
    """
    not_started, in_progress, done = get_items_by_status()
    return not_started + in_progress + done


def get_items_by_status():
    """
    Fetches all saved items from Trello, partitioned by status.

    Returns:
        not_started: The list of items with Not Started status
        in_progress: The list of items with In Progress status
        done: The list of items with Done status
    """
    lists_response = trello_repository.fetch_lists()
    not_started = map_cards_for_status(lists_response, Status.NOT_STARTED)
    in_progress = map_cards_for_status(lists_response, Status.IN_PROGRESS)
    done = map_cards_for_status(lists_response, Status.DONE)
    return not_started, in_progress, done


def get_item(id):
    """
    Fetches the saved item with the specified ID from Trello.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item.id == id), None)


def add_item(title):
    """
    Adds a new item with the specified title to Trello with not started status.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    trello_repository.create_card(title)


def update_status(id, status):
    """
    Updates the status of existing item in Trello.

    Args:
        id: The Trello ID of the item
        status: The new status of the item to update
    """
    trello_repository.update_status(id, status)


def delete_item(id):
    """
    Deletes the item with the specified ID from Trello.

    Args:
        id: The ID of the item.
    """
    trello_repository.delete_card(id)


def map_cards_for_status(response, status):
    """
    Maps cards of a given status from Trello lists response to display class.

    Args:
        response: The response from the Trello lists endpoint.
        status: The status of the cards to map and return.

    Returns:
        items: An list of mapped Item objects with the given status.
    """
    list_id = trello_repository.get_list_id_for_status(status)
    trello_cards = next(
        list for list in response if list["id"] == list_id
    )["cards"]
    return [Item.from_trello_card(card, status) for card in trello_cards]
