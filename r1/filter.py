import datetime as dt
import functools as ft

from .helpers import (first_day_of_this_week, today)
from .types import (DishType, Restaurant)


def void_filter(_):
    return True


def item_filter(attr, value):
    if value is None:
        return void_filter

    def item_filter_impl(menu_item):
        return getattr(menu_item, attr) == value

    return item_filter_impl


date_filter = ft.partial(item_filter, 'date')
rest_filter = ft.partial(item_filter, 'restaurant')
type_filter = ft.partial(item_filter, 'type')


def chain_filters(*args):
    def chain_filters_impl(menu_item):
        return all(f(menu_item) for f in args)

    return chain_filters_impl


def day_of_this_week(day):
    return first_day_of_this_week() + dt.timedelta(days=day)


filters = {
    'week': void_filter,
    'today': date_filter(today()),
    'tomorrow': date_filter(today() + dt.timedelta(days=1)),
    'monday': date_filter(day_of_this_week(0)),
    'tuesday': date_filter(day_of_this_week(1)),
    'wednesday': date_filter(day_of_this_week(2)),
    'thursday': date_filter(day_of_this_week(3)),
    'friday': date_filter(day_of_this_week(4)),

    'r1': rest_filter(Restaurant.r1),
    'r2': rest_filter(Restaurant.r2),
	'r3': rest_filter(Restaurant.r3),

    'menu1': type_filter(DishType.menu1),
    'menu2': type_filter(DishType.menu2),
    'vegetarian': type_filter(DishType.vegetarian),
    'speciality': type_filter(DishType.speciality),
    'grill': type_filter(DishType.grill),
    'pasta': type_filter(DishType.pasta),
    'pizza': type_filter(DishType.pizza)
}


def make_filter(strings):
    return chain_filters(*[filters.get(s, void_filter) for s in strings])


def filter_menu(menu, filter_):
    return [mi for mi in menu if filter_(mi)]
