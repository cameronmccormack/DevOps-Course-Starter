from flask import Flask
from flask import render_template, redirect
from flask.globals import request
from flask_login import LoginManager, login_required, login_user, current_user
import requests

from todo_app.auth.decorators import requireWriter
from todo_app.auth.user_roles import UserRoles
from todo_app.data.mongo_db_items import MongoDbItemProvider as ItemProvider
from todo_app.flask_config import Config
from todo_app.models.status import Status
from todo_app.models.view_model import ViewModel
from todo_app.auth.user import User


def create_app():
    app = Flask(__name__)
    config = Config()
    app.config.from_object(config)
    item_provider = ItemProvider()
    login_manager = LoginManager()

    @login_manager.unauthorized_handler
    def unauthenticated():
        return redirect(config.GITHUB_LOGIN_URL)

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    @app.route('/')
    @login_required
    def index():
        not_started, in_progress, done = item_provider.get_items_by_status()
        show_all_items = (
            True if (request.args.get("show_all_items") == "true") else False
        )
        item_view_model = ViewModel(
            not_started,
            in_progress,
            done,
            current_user.is_anonymous or current_user.role == UserRoles.WRITER,
            show_all_items
        )
        return render_template('index.html', view_model=item_view_model)

    @app.route('/showHiddenItems/')
    @login_required
    def show_hidden_items():
        return redirect('/?show_all_items=true')

    @app.route('/hideExpandedItems/')
    @login_required
    def hide_exapanded_items():
        return redirect('/?show_all_items=false')

    @app.route('/addItem', methods=['POST'])
    @login_required
    @requireWriter
    def add_item():
        item = request.form.get('add-item')
        item_provider.add_item(item)
        return redirect('/')

    @app.route('/markNotStarted/<id>', methods=['POST'])
    @login_required
    @requireWriter
    def mark_not_started(id):
        item_provider.update_status(id, Status.NOT_STARTED)
        return redirect('/')

    @app.route('/markInProgress/<id>', methods=['POST'])
    @login_required
    @requireWriter
    def mark_in_progress(id):
        item_provider.update_status(id, Status.IN_PROGRESS)
        return redirect('/')

    @app.route('/markDone/<id>', methods=['POST'])
    @login_required
    @requireWriter
    def mark_done(id):
        item_provider.update_status(id, Status.DONE)
        return redirect('/')

    @app.route('/delete/<id>', methods=['POST'])
    @login_required
    @requireWriter
    def delete_item(id):
        item_provider.delete_item(id)
        return redirect('/')

    @app.route('/login/callback')
    def user_login():
        auth_params = {
            "client_id": config.GITHUB_CLIENT_ID,
            "client_secret": config.GITHUB_CLIENT_SECRET,
            "code": request.args.get("code")
        }

        access_token = requests.post(
            "https://github.com/login/oauth/access_token",
            params=auth_params,
            headers={"Accept": "application/json"}
        ).json()["access_token"]

        user_id = requests.get(
            "https://api.github.com/user",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
        ).json()["id"]

        user = User(user_id)
        login_user(user)

        return redirect('/')

    login_manager.init_app(app)
    return app
