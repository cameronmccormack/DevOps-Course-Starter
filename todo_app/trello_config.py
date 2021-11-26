import os


class Config:
    def __init__(self):
        """Variables for integration with Trello API."""
        self.TRELLO_API_KEY = os.environ.get('TRELLO_API_KEY')
        if not self.TRELLO_API_KEY:
            raise ValueError("No TRELLO_API_KEY set for Trello integration.")

        self.TRELLO_TOKEN = os.environ.get('TRELLO_TOKEN')
        if not self.TRELLO_TOKEN:
            raise ValueError("No TRELLO_TOKEN set for Trello integration.")

        self.BOARD_ID = os.environ.get('BOARD_ID')
        if not self.BOARD_ID:
            raise ValueError("No BOARD_ID set for Trello integration.")

        self.NOT_STARTED_LIST_ID = os.environ.get('NOT_STARTED_LIST_ID')
        if not self.NOT_STARTED_LIST_ID:
            raise ValueError(
                "No NOT_STARTED_LIST_ID set for Trello integration."
            )

        self.IN_PROGRESS_LIST_ID = os.environ.get('IN_PROGRESS_LIST_ID')
        if not self.IN_PROGRESS_LIST_ID:
            raise ValueError(
                "No IN_PROGRESS_LIST_ID set for Trello integration."
            )

        self.DONE_LIST_ID = os.environ.get('DONE_LIST_ID')
        if not self.DONE_LIST_ID:
            raise ValueError("No DONE_LIST_ID set for Trello integration.")

        self.BASE_URL = os.environ.get('TRELLO_BASE_URL')
        if not self.BASE_URL:
            raise ValueError("No TRELLO_BASE_URL set for Trello integration.")
