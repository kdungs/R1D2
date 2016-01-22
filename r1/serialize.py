import itertools as it


def serialize_attr(name, value):
    if name in ('restaurant', 'type'):
        return value.name
    if name == 'date':
        return str(value)
    return value


def serialize_item(item, attrs):
    return {attr: serialize_attr(attr, getattr(item, attr)) for attr in attrs}


def serialize_menu(menu):
    attrs = ['restaurant', 'date', 'type', 'name', 'price']
    return [serialize_item(item, attrs) for item in menu]
