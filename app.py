import r1

from datetime import (date, timedelta)
from flask import (Flask, jsonify, g)
from flask.ext import shelve

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
    print(day)
    print(fd)
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
    if not days.has_key(day):
        return jsonify(error=True)
    return jsonify(menu=menu()[days[day]])


if __name__ == "__main__":
    app.run(debug=True)
