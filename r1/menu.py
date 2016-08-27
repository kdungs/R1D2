from datetime import timedelta
import bs4
import itertools as it
import re
import requests

from .helpers import (first_day_of_this_week, grouper, today)
from .settings import (PARAMS, URL1, URL2)
from .types import (DishType, MenuItem, Restaurant)


def get_urls(restaurant):
    params = PARAMS[restaurant]
    return (URL1.format(**params), URL2.format(**params))


def extract_name(bsitem):
    return bsitem.find('span').text


def extract_price(bsitem):
    reg = re.compile(r'(\d+\.?\d*)')
    mat = reg.findall(bsitem.text)
    if len(mat) > 0:
        return float(mat[0])
    return 0.0


def extract_table(response):
    items = bs4.BeautifulSoup(response.text, 'lxml').find(
        'table',
        class_='menuRestaurant').findAll('table',
                                         class_='HauteurMenu')
    return [(extract_name(i), extract_price(i)) for i in items[1::2]]


def create_payload(page):
    return {'fa_afficheSemaine_menurestaurant': 'Page {}'.format(page),
            'fn_changeType': 2,
            'fn_jourSemaine': '{}'.format(today()),
            'fn_limite': 2 * page - 1,
            'fn_refresh': 1,
            'fn_numpage': page}


def fetch_menu(restaurant):
    url1, url2 = get_urls(restaurant)
    params = PARAMS[restaurant]
    s = requests.Session()
    return it.chain([extract_table(s.get(url1))] +
                    [extract_table(s.post(url2,
                                          data=create_payload(i)))
                     for i in range(2, params.get('pages', 2) + 1)])


def split_days(items, structure):
    xs = [grouper(i, n) for i, n in zip(items, structure)]
    return [list(it.chain(*i)) for i in zip(*xs)]


def get_menu(restaurant):
    params = PARAMS[restaurant]
    items = split_days(fetch_menu(restaurant), params['page_structure'])
    day_structure = params['dishes']
    first_day = first_day_of_this_week()
    menu = []
    for d, ms in enumerate(items):
        day = first_day + timedelta(days=d)
        for (name, price), t in zip(ms, day_structure):
            menu.append(MenuItem(restaurant, day, t, name, price))
    return menu


def get_full_menu():
    return get_menu(Restaurant.r1) + get_menu(Restaurant.r2) + get_menu(Restaurant.r3)
