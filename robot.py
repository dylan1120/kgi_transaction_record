from json import dumps
from httplib2 import Http
import config


def robot(content):
    """Hangouts Chat incoming webhook quickstart."""
    url = config.robot["tsaitung"]
    bot_message = {
        'text' : content }

    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

    http_obj = Http()

    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )

def robot_kgi(content):
    """Hangouts Chat incoming webhook quickstart."""
    url = config.robot["KGI"]
    bot_message = {
        'text' : content }

    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

    http_obj = Http()

    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )