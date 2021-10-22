from flask import Flask
from flask import render_template, redirect
from flask.globals import request

from todo_app.data import session_items
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = session_items.get_items()
    return render_template('index.html', items=items)

@app.route('/addItem', methods=['POST'])
def add_item():
    item = request.form.get('add-item')
    session_items.add_item(item)
    return redirect('/')
