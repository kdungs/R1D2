def void_filter(_):
    return True


def item_filter(attr, value):
    if value is None:
        return void_filter

    def item_filter_impl(menu_item):
        return getattr(menu_item, attr) == value

    return item_filter_impl


def chain_filters(*args):
    def chain_filters_impl(menu_item):
        return all(f(menu_item) for f in args)

    return chain_filters_impl


def compose_filter(**kwargs):
    return chain_filters(*[make_filter(k, v) for k, v in kwargs])


def filter_menu(menu, filter_):
    return [mi for mi in menu if filter_(mi)]
