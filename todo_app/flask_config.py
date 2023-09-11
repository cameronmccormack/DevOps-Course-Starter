import os


class Config:
    def __init__(self):
        """Base configuration variables."""
        self.SECRET_KEY = os.environ.get('SECRET_KEY')
        if not self.SECRET_KEY:
            self.throw_missing_env_error('SECRET_KEY')

        self.GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
        if not self.GITHUB_CLIENT_ID:
            self.throw_missing_env_error('GITHUB_CLIENT_ID')

        self.GITHUB_LOGIN_URL = (
            "https://github.com/login/oauth/authorize" +
            f"?client_id={self.GITHUB_CLIENT_ID}"
        )

        self.GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')
        if not self.GITHUB_CLIENT_SECRET:
            self.throw_missing_env_error('GITHUB_CLIENT_SECRET')

        self.LOGIN_DISABLED = os.environ.get('LOGIN_DISABLED') == 'True'

        self.LOG_LEVEL = os.environ.get('LOG_LEVEL')
        if not self.LOG_LEVEL:
            self.throw_missing_env_error('LOG_LEVEL')

        self.LOGGLY_TOKEN = os.environ.get('LOGGLY_TOKEN')

    def throw_missing_env_error(key):
        raise ValueError(
                f"No {key} set for Flask application. " +
                "Did you follow the setup instructions?"
            )
