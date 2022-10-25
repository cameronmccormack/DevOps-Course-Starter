from todo_app.repository.mongo_db_repository import MongoDbRepository
from todo_app.models.item import Item
from todo_app.models.status import Status


class MongoDbItemProvider:
    def __init__(self):
        self.mongo_db_repository = MongoDbRepository()

    def get_items_by_status(self):
        """
        Fetches all saved items from MongoDb, partitioned by status.

        Returns:
            not_started: The list of items with Not Started status
            in_progress: The list of items with In Progress status
            done: The list of items with Done status
        """
        not_started = self.get_items_as_display_class(
            Status.NOT_STARTED
        )
        in_progress = self.get_items_as_display_class(
            Status.IN_PROGRESS
        )
        done = self.get_items_as_display_class(
            Status.DONE
        )
        return not_started, in_progress, done

    def add_item(self, title):
        """
        Adds a new item with the specified title to MongoDB with not started
        status.

        Args:
            title: The title of the item.

        Returns:
            item: The saved item.
        """
        self.mongo_db_repository.create_card(title)

    def update_status(self, id, status):
        """
        Updates the status of existing item in MongoDB.

        Args:
            id: The ID of the item
            status: The new status of the item to update
        """
        self.mongo_db_repository.update_status(id, status)

    def delete_item(self, id):
        """
        Deletes the item with the specified ID from MongoDB.

        Args:
            id: The ID of the item.
        """
        self.mongo_db_repository.delete_card(id)

    def get_items_as_display_class(self, status):
        """
        Maps card items from MongoDB to display class.

        Args:
            mongo_db_items: The card items from MongoDB.

        Returns:
            items: An list of mapped Item objects with the given status.
        """
        items = self.mongo_db_repository.get_all_cards_for_status(
            status
        )
        return [Item.from_mongo_db_item(card) for card in items]
