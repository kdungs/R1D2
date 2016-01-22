import datetime as dt
import functools as ft

from r1.helpers import (first_day_of_this_week, today)
from r1.types import (DishType, Restaurant)
from r1.filter import (chain_filters, item_filter, void_filter)


date_filter = ft.partial(item_filter, 'date')
rest_filter = ft.partial(item_filter, 'restaurant')
type_filter = ft.partial(item_filter, 'type')


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
