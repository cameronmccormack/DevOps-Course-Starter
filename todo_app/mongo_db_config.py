import os


class Config:
    def __init__(self):
        """Variables for integration with MongoDB."""
        self.DB_PRIMARY_CONNECTION_STRING = os.environ.get(
            'DB_PRIMARY_CONNECTION_STRING'
        )
        if not self.DB_PRIMARY_CONNECTION_STRING:
            raise ValueError(
                "No DB_PRIMARY_CONNECTION_STRING set for MongoDB integration."
            )

        self.DB_NAME = os.environ.get('DB_NAME')
        if not self.DB_NAME:
            raise ValueError("No DB_NAME set for MongoDB integration.")
