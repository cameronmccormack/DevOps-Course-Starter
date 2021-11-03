from flask import Flask
from flask import render_template, redirect
from flask.globals import request

from todo_app.data import session_items
from todo_app.flask_config import Config
from todo_app.models.status import Status

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    not_started, in_progress, done = session_items.get_items_by_status()
    return render_template(
        'index.html',
        not_started=not_started,
        in_progress=in_progress,
        done=done
    )


@app.route('/addItem', methods=['POST'])
def add_item():
    item = request.form.get('add-item')
    session_items.add_item(item)
    return redirect('/')


@app.route('/markNotStarted/<id>', methods=['POST'])
def mark_not_started(id):
    item = session_items.get_item(id)
    item['status'] = Status.NOT_STARTED
    session_items.save_item(item)
    return redirect('/')


@app.route('/markInProgress/<id>', methods=['POST'])
def mark_in_progress(id):
    item = session_items.get_item(id)
    item['status'] = Status.IN_PROGRESS
    session_items.save_item(item)
    return redirect('/')


@app.route('/markDone/<id>', methods=['POST'])
def mark_done(id):
    item = session_items.get_item(id)
    item['status'] = Status.DONE
    session_items.save_item(item)
    return redirect('/')


@app.route('/delete/<id>', methods=['POST'])
def delete_item(id):
    session_items.delete_item(id)
    return redirect('/')
