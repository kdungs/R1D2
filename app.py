import r1

from datetime import (date, timedelta)
from flask import (Flask, jsonify, g, request)
from flask.ext import shelve
from os import getenv

TELEGRAM_BOT_TOKEN = getenv('TELEGRAM_BOT_TOKEN')

app = Flask(__name__)
app.config['SHELVE_FILENAME'] = 'shelve.db'
shelve.init_app(app)


def first_day_of_this_week():
    today = date.today()
    return today - timedelta(days=today.weekday())


def load_menu():
    db = shelve.get_shelve()
    fd = first_day_of_this_week()
    day = db.get('day', None)
    if day is None or day != fd:
        db['menu'] = r1.get_menu()
        db['day'] = fd
    return db['menu']


def menu():
    d = g.get('day', None)
    fd = first_day_of_this_week()
    if d is None or d != fd:
        g.menu = load_menu()
        g.day = d
    return g.menu


def format_menu(day, menu):
    return '*{day}*\n{items}'.format(
        day=day,
        items='\n'.join(['{} _(CHF {:.2f})_'.format(name, price)
                         for name, price in menu]))


def telegram_response(chat_id, text, **kwargs):
    return jsonify(method='sendMessage', chat_id=chat_id, text=text, **kwargs)


@app.route('/telegram/{}/'.format(TELEGRAM_BOT_TOKEN), methods=['POST'])
def handle_telegram():
    data = request.json
    if 'message' not in data:
        return 'OK'
    msg = data['message']
    chatid = msg['chat']['id']
    command = msg.get('text')
    if command is None or command[0] != '/':
        return 'OK'
    if command == '/today':
        wd = date.today().weekday()
        if wd > 4:
            return telegram_response(chatid, "It's the weekend. :)")
        else:
            return telegram_response(chatid,
                                     format_menu(day='Today',
                                                 menu=menu()[wd]),
                                     parse_mode='Markdown')
    else:
        return 'OK'


@app.route("/")
@app.route("/today")
def menu_for_today():
    wd = date.today().weekday()
    if wd > 4:
        return jsonify(day='today', message="It's the weekend!")
    return jsonify(day='today', menu=menu()[wd])


@app.route("/week")
def menu_for_week():
    return jsonify(menu=menu())


@app.route("/<day>")
def menu_for_day(day):
    days = {'monday': 0,
            'tuesday': 1,
            'wednesday': 2,
            'thursday': 3,
            'friday': 4}
    if day not in days:
        return jsonify(error=True)
    return jsonify(menu=menu()[days[day]])


if __name__ == "__main__":
    app.run(debug=True)
