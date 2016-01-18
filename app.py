from flask import (Flask, jsonify)
import r1
from datetime import (date, timedelta)
from werkzeug.contrib.cache import SimpleCache

app = Flask(__name__)
cache = SimpleCache()


def first_day_of_this_week():
    today = date.today()
    return today - timedelta(days=today.weekday())


def menu():
    return cache.get('menu')


@app.before_request
def load_menu():
    d = cache.get('day')
    fd = first_day_of_this_week()
    if d is None or d != fd:
        menu = r1.get_menu()
        cache.set('day', fd)
        cache.set('menu', menu)


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
