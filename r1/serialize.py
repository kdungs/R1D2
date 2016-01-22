import itertools as it


def split_by(items, attr):
    fn = lambda item: getattr(item, attr)
    items = sorted(items, key=fn)
    return it.groupby(items, key=fn)


def serialize_attr(name, value):
    if name in ('restaurant', 'type'):
        return value.name
    if name == 'date':
        return str(value)
    return value


def serialize_item(item, attrs):
    return {attr: serialize_attr(attr, getattr(item, attr)) for attr in attrs}


def serialize_menu(menu, structure, attrs=None):
    if attrs is None:
        attrs = ['restaurant', 'date', 'type', 'name', 'price']
    if len(structure) == 0:
        return [serialize_item(item, attrs) for item in menu]
    head = structure[0]
    tail = structure[1:]
    attrs = [a for a in attrs if a != head]
    return {serialize_attr(head, k): serialize_menu(v, tail, attrs)
            for k, v in split_by(menu, head)}
