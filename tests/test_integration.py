import pytest
from dotenv import load_dotenv, find_dotenv
import os
import requests


from todo_app import app


@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')

    load_dotenv(file_path, override=True)
    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client


def test_index_page(client, monkeypatch):
    monkeypatch.setattr(requests, 'get', get_lists_stub)
    response = client.get('/')
    assert response.status_code == 200
    assert 'Test not started card' in response.data.decode()
    assert 'Test in progress card' in response.data.decode()
    assert 'Test done card' in response.data.decode()


class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data


def get_lists_stub(url):
    test_board_id = os.environ.get('BOARD_ID')

    not_started_list_id = os.environ.get('NOT_STARTED_LIST_ID')
    in_progress_list_id = os.environ.get('IN_PROGRESS_LIST_ID')
    done_list_id = os.environ.get('DONE_LIST_ID')

    trello_url = os.environ.get('TRELLO_BASE_URL')
    trello_key = os.environ.get('TRELLO_API_KEY')
    trello_token = os.environ.get('TRELLO_TOKEN')

    query_string = f'?key={trello_key}&token={trello_token}&cards=open'

    fake_response_data = None

    if (url == f'{trello_url}boards/{test_board_id}/lists{query_string}'):
        fake_response_data = [
            {
                'id': not_started_list_id,
                'name': 'Not Started',
                'cards': [{
                    'id': '123',
                    'name': 'Test not started card',
                    'dateLastActivity': '2007-03-01T13:00:00Z'
                }]
            },
            {
                'id': in_progress_list_id,
                'name': 'In Progress',
                'cards': [{
                    'id': '123',
                    'name': 'Test in progress card',
                    'dateLastActivity': '2007-03-01T13:00:00Z'
                }]
            },
            {
                'id': done_list_id,
                'name': 'Done',
                'cards': [{
                    'id': '123',
                    'name': 'Test done card',
                    'dateLastActivity': '2007-03-01T13:00:00Z'
                }]
            },
        ]
        return StubResponse(fake_response_data)
