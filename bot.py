import r1
from r1.filter import make_filter

def telegram_response(chat_id, text, **kwargs):
    return dict(method='sendMessage', chat_id=chat_id, text=text, **kwargs)


def parse_request(request):
    chat_id = get_(request, 'message', 'chat', 'id')
    command = get_(request, 'message', 'text')
    if command is None or not command.startswith('/'):
        Warning('Received invalid command. Will be ignored.')
        return chat_id, None
    return chat_id, command[1:]


def get_(dict_, *keys, default=None):
    if dict_ is None:
        return default
    elem = dict_.get(keys[0], default)
    if len(keys) == 1:
        return elem
    return get_(elem, *keys[1:], default=default)


class SimpleBot:
    def __init__(self, telegram_params=None):
        self.actions = {}
        if telegram_params is None:
            telegram_params = {}
        self.telegram_params = telegram_params

    def add_action(self, name, target):
        if name in self.actions:
            Warning(
                'Action `{}` was already defined. Will be overwritten.'.format(
                    name))
        self.actions[name] = target

    def _sanitize_action(self, action):
        if '@' in action:
            return action.split('@')[0]
        return action

    def _split_command(self, cmd):
        cmd = cmd.split()
        return cmd[0], cmd[1:]

    def handle(self, command, request):
        action, options = self._split_command(command)
        action = self._sanitize_action(action)
        if action not in self.actions:
            Warning('Undefined action `{}`. Will be ignored.'.format(action))
            return None
        return self.actions[action](options, request)

    def respond(self, request):
        chat_id, command = parse_request(request)
        if chat_id is None or command is None:
            return None
        response = self.handle(command, request)
        if response is None:
            return None
        return telegram_response(chat_id, response, **self.telegram_params)


def format_item(sitem):
    return '{type}: {name} _(CHF {price:.2f})_'.format(
        type=sitem['type'].capitalize(),
        name=sitem['name'],
        price=sitem['price']
    )


def format_menu(items):
    if len(items) == 0:
        return 'There was no menu for your request.'
    sitems = r1.serialize_menu(items)
    return '\n'.join(format_item(sitem) for sitem in sitems)


class RestaurantBot(SimpleBot):
    def __init__(self, menu_getter, *args, **kwargs):
        super().__init__(*args, telegram_params={'parse_mode': 'Markdown'},
                         **kwargs)
        self.get_menu = menu_getter

    def _menu_action(self, filters):
        def menu_action_impl(options, _):
            filter_ = make_filter(filters + options)
            return format_menu(r1.filter_menu(self.get_menu(), filter_))

        return menu_action_impl

    def add_menu_action(self, command, filters):
        self.add_action(command, self._menu_action(filters))
