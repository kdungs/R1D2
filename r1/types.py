from enum import Enum
from collections import namedtuple
from functools import partial


def valid_string_for_enum(enum, s):
    return s in enum.__members__


def enum_from_string(enum, s):
    return enum.__members__[s]


Restaurant = Enum('Restaurant', ['r1', 'r2', 'r3'])
valid_string_for_restaurant = partial(valid_string_for_enum, Restaurant)
restaurant_from_string = partial(enum_from_string, Restaurant)


DishType = Enum('DishType', ['menu1', 'menu2', 'menu3', 'vegetarian',
                             'speciality', 'grill', 'pasta', 'pizza'])
valid_string_for_dishtype = partial(valid_string_for_enum, DishType)
dishtype_from_string = partial(enum_from_string, DishType)


MenuItem = namedtuple('MenuItem', ['restaurant', 'date', 'type',
                                   'name', 'price'])
