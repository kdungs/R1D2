import os
import requests

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
BASEURL = 'https://api.telegram.org/bot' + TOKEN


def sendMessage(chat_id, text, **kwargs):
    kwargs['chat_id'] = chat_id
    kwargs['text'] = text
    r = requests.post(BASEURL + '/sendMessage', json=kwargs)
    return r.ok
