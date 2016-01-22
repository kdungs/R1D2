import bs4
import collections
import datetime as dt
import enum
import functools as ft
import itertools as it
import re
import requests

DishType = enum.Enum('DishType', ['menu1', 'menu2', 'vegetarian', 'speciality',
                                  'grill', 'pasta', 'pizza'])


def valid_string_for_dish_type(s):
    return s in DishType.__members__


def dish_type_from_string(s):
    dt = DishType.__members__.get(s)
    return dt


MenuItem = collections.namedtuple('MenuItem', ['restaurant', 'date', 'type',
                                               'name', 'price'])

BASE = 'http://extranet.novae-restauration.ch/'
PARAMS = {
    'r1': {
        'x': 'd894ddae3c17b40b4fe7e16519f950f0',
        'y': 'c7b3f79848b99a8e562a1df1d6285365',
        'z': '33',
        'html': 'restaurant-cern',
        'pages': 3,
        'page_structure': (3, 2, 2),
        'dishes': (DishType.menu1, DishType.menu2, DishType.vegetarian,
                   DishType.speciality, DishType.grill, DishType.pasta,
                   DishType.pizza)
    },
    'r2': {
        'x': 'ad3f8f75fe1e353b972afcce8e375d6e',
        'y': '81dc9bdb52d04dc20036dbd8313ed055',
        'z': '135',
        'html': 'bon-app',
        'pages': 2,
        'page_structure': (3, 3),
        'dishes': (DishType.menu1, DishType.menu2, DishType.vegetarian,
                   DishType.grill, DishType.pizza, DishType.speciality)
    }
}
URL1 = BASE + 'index.php?frame=1&x={x}&y={y}&z={z}'
URL2 = BASE + '/novae/traiteur/restauration/{html}.html?frame=1'


def get_urls(restaurant):
    params = PARAMS[restaurant]
    return (URL1.format(**params), URL2.format(**params))


def extract_name(bsitem):
    return bsitem.find('span').text


def extract_price(bsitem):
    reg = re.compile(r'([\d\.]+)')
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
            'fn_jourSemaine': '{}'.format(dt.date.today()),
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


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return it.zip_longest(*args, fillvalue=fillvalue)


def split_days(items, structure):
    xs = [grouper(i, n) for i, n in zip(items, structure)]
    return [list(it.chain(*i)) for i in zip(*xs)]


def first_day_of_this_week():
    today = dt.date.today()
    return today - dt.timedelta(days=today.weekday())


def get_menu(restaurant):
    params = PARAMS[restaurant]
    items = split_days(fetch_menu(restaurant), params['page_structure'])
    day_structure = params['dishes']
    first_day = first_day_of_this_week()
    menu = []
    for d, ms in enumerate(items):
        day = first_day + dt.timedelta(days=d)
        for (name, price), t in zip(ms, day_structure):
            menu.append(MenuItem(restaurant, day, t, name, price))
    return menu
