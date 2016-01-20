#!/usr/bin/env python

import argparse
import requests
import sys

URL = 'https://r1d2.herokuapp.com'


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


def fetch_week():
    return get_menu(get_json(URL + '/week'))


def show_today():
    print_menu(fetch_today())


def show_day(day):
    day = day.lower()
    j = get_json(URL + '/{}'.format(day))
    if 'error' in j:
        print('Could not fetch menu for day = {}'.format(day))
    print_menu(get_menu(j), day=day.capitalize())


def show_week():
    days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday')
    menus = fetch_week()
    for day, menu in enumerate(menus):
        print_menu(menu, days[day])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch menu of R1 at CERN')
    parser.add_argument(
        '--day',
        help='Get menu for specific day (Monday through Friday).')
    parser.add_argument('--week',
                        action='store_true',
                        help='Get menu for the whole week.')
    args = parser.parse_args()

    if args.week:
        show_week()
    elif args.day is not None:
        show_day(args.day)
    else:
        show_today()
