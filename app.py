import r1
from r1.helpers import (first_day_of_this_week)
from r1.filter import (filter_menu, make_filter)

from flask import (Flask, jsonify, g, request)
from flask.ext import shelve
from os import getenv
from functools import partial

TELEGRAM_BOT_TOKEN = getenv('TELEGRAM_BOT_TOKEN')

app = Flask(__name__)
app.debug = True
app.config['SHELVE_FILENAME'] = 'shelve.db'
shelve.init_app(app)


def load_menu():
    db = shelve.get_shelve()
    fd = first_day_of_this_week()
    day = db.get('day', None)
    if day is None or day != fd:
        db['menu'] = r1.get_full_menu()
        db['day'] = fd
    return db['menu']


def get_menu():
    d = g.get('day', None)
    fd = first_day_of_this_week()
    if d is None or d != fd:
        g.menu = load_menu()
        g.day = d
    return g.menu


def get_(dict_, *keys, default=None):
    if dict_ is None:
        return default
    elem = dict_.get(keys[0], default)
    if len(keys) == 1:
        return elem
    return get_(elem, *keys[1:], default=default)


def telegram_response(chat_id, text, **kwargs):
    return jsonify(method='sendMessage', chat_id=chat_id, text=text, **kwargs)


@app.route('/telegram/{}/'.format(TELEGRAM_BOT_TOKEN), methods=['POST'])
def handle_telegram():
    chat_id = get_(request.json, 'message', 'chat', 'id')
    if chat_id is None:
        return 'OK'
    response = partial(telegram_response, chat_id, parse_mode='Markdown')
    command = get_(request.json, 'message', 'text')
    if command is None or not command.startswith('/'):
        return 'OK'
    menu = get_menu()
    cmd = command[1:]
    menu = filter_menu(menu, make_filter([cmd, 'today']))
    return response("""Hello, friend!
R1D2 went skiing over the weekend and will be back on Monday.""")


@app.route('/<path:path>')
def json_menu(path):
    filter_ = make_filter(path.split('/'))
    menu = filter_menu(get_menu(), filter_)
    return jsonify(menu=r1.serialize_menu(menu))


@app.route('/')
def index():
    return json_menu('today')


if __name__ == "__main__":
    app.run(debug=True)
