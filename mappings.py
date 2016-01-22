import datetime as dt
from r1.helpers import (first_day_of_this_week, today)
from r1.types import (DishType, Restaurant)


def day_of_this_week(day):
    return first_day_of_this_week() + dt.timedelta(days=day)


DAYS = {'today': today(),
        'tomorrow': today() + dt.timedelta(days=1),
        'monday': day_of_this_week(0),
        'tuesday': day_of_this_week(1),
        'wednesday': day_of_this_week(2),
        'thursday': day_of_this_week(3),
        'friday': day_of_this_week(4)}

RESTAURANTS = {'r1': Restaurant.r1,
               'r2': Restaurant.r2}

DISHTYPES = DishType.__members__
