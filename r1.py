from datetime import date
import bs4
import itertools as it
import re
import requests

BASE = 'http://extranet.novae-restauration.ch/'
PARAMS = {'x': 'd894ddae3c17b40b4fe7e16519f950f0',
          'y': 'c7b3f79848b99a8e562a1df1d6285365',
          'z': '33'}
URL1 = BASE + 'index.php?frame=1&x={x}&y={y}&z={z}'.format(**PARAMS)
URL2 = BASE + '/novae/traiteur/restauration/restaurant-cern.html?frame=1'


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return it.zip_longest(*args, fillvalue=fillvalue)


def extract_name(bsitem):
    return bsitem.find('span').text


def extract_price(bsitem):
    reg = re.compile(r'CHF ([\d\.]+)')
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
            'fn_jourSemaine': '{}'.format(date.today()),
            'fn_limite': 2 * page - 1,
            'fn_refresh': 1,
            'fn_numpage': page}


def split_days(items):
    xs = [grouper(i, n) for i, n in zip(items, (3, 2, 2))]
    return [list(it.chain(*i)) for i in zip(*xs)]


def get_menu():
    s = requests.Session()
    return split_days([extract_table(s.get(URL1)),
                       extract_table(s.post(URL2, data=create_payload(2))),
                       extract_table(s.post(URL2, data=create_payload(3)))])
