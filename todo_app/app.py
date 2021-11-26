from flask import Flask
from flask import render_template, redirect
from flask.globals import request

from todo_app.data import trello_items as item_service
from todo_app.flask_config import Config
from todo_app.models.status import Status

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    not_started, in_progress, done = item_service.get_items_by_status()
    return render_template(
        'index.html',
        not_started=not_started,
        in_progress=in_progress,
        done=done
    )


@app.route('/addItem', methods=['POST'])
def add_item():
    item = request.form.get('add-item')
    item_service.add_item(item)
    return redirect('/')


@app.route('/markNotStarted/<id>', methods=['POST'])
def mark_not_started(id):
    item_service.update_status(id, Status.NOT_STARTED)
    return redirect('/')


@app.route('/markInProgress/<id>', methods=['POST'])
def mark_in_progress(id):
    item_service.update_status(id, Status.IN_PROGRESS)
    return redirect('/')


@app.route('/markDone/<id>', methods=['POST'])
def mark_done(id):
    item_service.update_status(id, Status.DONE)
    return redirect('/')


@app.route('/delete/<id>', methods=['POST'])
def delete_item(id):
    item_service.delete_item(id)
    return redirect('/')
