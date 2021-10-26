from flask import session
from todo_app.models.status import Status


def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
    return session.get('items', [])


def get_items_by_status():
    """
    Fetches all saved items from the session, partitioned by status.

    Returns:
        not_started: The list of items with Not Started status
        in_progress: The list of items with In Progress status
        done: The list of items with Done status
    """
    items = get_items()
    not_started, in_progress, done = [], [], []
    for item in items:
        if (item['status'] == Status.DONE):
            done.append(item)
        elif (item['status'] == Status.IN_PROGRESS):
            in_progress.append(item)
        else:
            not_started.append(item)
    return not_started, in_progress, done


def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item['id'] == int(id)), None)


def add_item(title):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    items = get_items()

    # Determine the ID for the item based on that of the previously added item
    id = items[-1]['id'] + 1 if items else 0

    item = {'id': id, 'title': title, 'status': Status.NOT_STARTED}

    # Add the item to the list
    items.append(item)
    session['items'] = items

    return item


def save_item(item):
    """
    Updates an existing item in the session. If no existing item matches the
    ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    existing_items = get_items()
    updated_items = [
        item if item['id'] == existing_item['id']
        else existing_item for existing_item in existing_items
    ]

    session['items'] = updated_items

    return item


def delete_item(id):
    """
    Deletes the item with the specified ID from the session.

    Args:
        id: The ID of the item.
    """
    existing_items = get_items()
    updated_items = [item for item in existing_items if item['id'] != int(id)]

    session['items'] = updated_items
