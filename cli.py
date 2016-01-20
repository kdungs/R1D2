#!/usr/bin/env python

import argparse
import requests
import sys
from datetime import date

URL = 'https://r1d2.herokuapp.com'
DAYS = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday')


def get_json(url):
    return requests.get(url).json()


def get_menu(json):
    return json['menu']


def format_item(name, price):
    return '{} (CHF {:.2f})'.format(name, price)


def print_menu(menu, day=None):
    if day is not None:
        print('--- {} ---'.format(day))
    for name, price in menu:
        print(format_item(name, price))


def fetch_today():
    return get_menu(get_json(URL))


def fetch_day(day):
    day = day.lower()
    j = get_json(URL + '/{}'.format(day))
    if 'error' in j:
        return None
    return get_menu(j)


def fetch_tomorrow():
    tomorrow = DAYS[(date.today().weekday() + 1) % 5]
    return fetch_day(tomorrow), tomorrow


def fetch_week():
    return get_menu(get_json(URL + '/week'))


def show_today():
    print_menu(fetch_today())


def show_day(day):
    menu = fetch_day(day)
    if menu is None:
        print('Could not fetch menu for day = {}'.format(day))
        return
    print_menu(menu, day=day.capitalize())


def show_tomorrow():
    print_menu(*fetch_tomorrow())


def show_week():
    menus = fetch_week()
    for day, menu in enumerate(menus):
        print_menu(menu, DAYS[day])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch menu of R1 at CERN')
    parser.add_argument(
        '--day',
        help='Get menu for specific day (Monday through Friday).')
    parser.add_argument('--tomorrow',
                        action='store_true',
                        help='Get menu for the next work day.')
    parser.add_argument('--week',
                        action='store_true',
                        help='Get menu for the whole week.')
    args = parser.parse_args()

    if args.tomorrow:
        show_tomorrow()
    elif args.week:
        show_week()
    elif args.day is not None:
        show_day(args.day)
    else:
        show_today()
