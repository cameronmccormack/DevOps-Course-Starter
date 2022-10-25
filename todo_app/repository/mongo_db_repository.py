from datetime import datetime
import pymongo
from bson import ObjectId

from todo_app.mongo_db_config import Config
from todo_app.models.status import Status

COLLECTION_NAME = "todo_items"


class MongoDbRepository:
    def __init__(self):
        self.config = Config()
        self.client = pymongo.MongoClient(
            self.config.DB_PRIMARY_CONNECTION_STRING
        )
        self.database = self.client[self.config.DB_NAME]
        self.collection = self.database[COLLECTION_NAME]

    def get_all_cards_for_status(self, status):
        cursor = self.collection.find(
            {"status": status}
        )
        return [item for item in cursor]

    def create_card(self, name):
        self.collection.insert_one({
            "name": name,
            "status": Status.NOT_STARTED,
            "last_status_change_datetime": datetime.now().isoformat()
        })

    def delete_card(self, id):
        self.collection.delete_one({
            "_id": id
        })

    def update_status(self, id, status):
        self.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "status": status,
                "last_status_change_datetime": datetime.now().isoformat()
            }}
        )
