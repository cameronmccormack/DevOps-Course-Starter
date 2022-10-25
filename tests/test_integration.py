import pytest
from dotenv import load_dotenv, find_dotenv
import mongomock
import pymongo


from todo_app import app
from todo_app.models.status import Status
from todo_app.mongo_db_config import Config


@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client


def test_index_page(client):
    config = Config()

    collection = pymongo.MongoClient(
        config.DB_PRIMARY_CONNECTION_STRING
    )[config.DB_NAME]["todo_items"]
    collection.insert_one({
        "name": "Test not started card",
        "status": Status.NOT_STARTED,
        "last_status_change_datetime": "2007-03-01T13:00:00Z"
    })
    collection.insert_one({
        "name": "Test in progress card",
        "status": Status.IN_PROGRESS,
        "last_status_change_datetime": "2007-03-01T13:00:00Z"
    })
    collection.insert_one({
        "name": "Test done card",
        "status": Status.DONE,
        "last_status_change_datetime": "2007-03-01T13:00:00Z"
    })

    response = client.get('/')
    assert response.status_code == 200
    assert 'Test not started card' in response.data.decode()
    assert 'Test in progress card' in response.data.decode()
    assert 'Test done card' in response.data.decode()
