from enum import Enum
from collections import namedtuple
from functools import partial


class OrderedEnum(Enum):
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


def valid_string_for_enum(enum, s):
    return s in enum.__members__


def enum_from_string(enum, s):
    return enum.__members__[s]


Restaurant = OrderedEnum('Restaurant', ['r1', 'r2'])
valid_string_for_restaurant = partial(valid_string_for_enum, Restaurant)
restaurant_from_string = partial(enum_from_string, Restaurant)


DishType = OrderedEnum('DishType', ['menu1', 'menu2', 'vegetarian',
                                    'speciality', 'grill', 'pasta', 'pizza'])
valid_string_for_dishtype = partial(valid_string_for_enum, DishType)
dishtype_from_string = partial(enum_from_string, DishType)


MenuItem = namedtuple('MenuItem', ['restaurant', 'date', 'type',
                                   'name', 'price'])
