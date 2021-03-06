from colorama import Fore, Back, Style, init
import time
import requests
import json
import threading

from RequestMap.Validators.ValidatorBase import StandardValidator
from RequestMap.Response.JSON import JSONStandardizer

init()

DISCORD_WEBHOOK_URLS = {}

def push_msg(messageType, *args, **kw):
    types = {
        'log': Style.DIM,
        'debug': Style.DIM,
        'info': Style.BRIGHT,
        'error': Fore.RED,
        'fatal': Fore.RED + Back.WHITE + Style.BRIGHT,
        'warning': Fore.YELLOW
    }
    print(types.get(messageType, ''), time.time(),
          '\t', *args, Style.RESET_ALL, **kw)
    # Pushes to Discord
    if DISCORD_WEBHOOK_URLS:
        threading.Thread(
            target=send_discord_msg,
            args=(messageType, *args),
            kwargs=kw
        ).start()


def send_discord_msg(messageType, *args, **kw):
    discord_colors = {
        'log': 0x000000,
        'debug': 0x000000,
        'info': 0x00FF00,
        'error': 0xFF0000,
        'fatal': 0xFF0000,
        'warning': 0xFFFF00
    }
    HOOK = DISCORD_WEBHOOK_URLS.get(messageType, DISCORD_WEBHOOK_URLS.get('default', None))
    if not HOOK:
        return

    r = requests.post(HOOK,
                      data=json.dumps({
                          'content': '',
                          'username': 'T2M Logs',
                          'embeds': [{
                              'title': messageType,
                              'description': 'Timestamp:' + str(time.time()),
                              'fields': [{
                                  'name': 'Message',
                                  'value': ' '.join(list(map(lambda x: str(x), args)))
                              }],
                              'color': discord_colors.get(messageType, 0x000000)
                          }]
                      }), headers={'Content-Type': 'application/json'})


def log(*args):
    push_msg('log', *args)


def debug(*args):
    push_msg('debug', *args)


def info(*args):
    push_msg('info', *args)


def error(*args):
    push_msg('error', *args)


def fatal(*args):
    push_msg('fatal',
             time.time(), *args)

def warning(*args):
    push_msg('warning', *args)


class Log(StandardValidator):
    def getEvaluationMethod(self, endpoint, protocolName):
        log('Calling', endpoint['endpointIdentifier'],
            'from protocol', protocolName + '.')

        def evaluate():  # Put required/optional arguments here
            return
        return evaluate

class JSONStandardizerWithLogs(JSONStandardizer):
    def exceptionHandler(self, exception, *, protocolName=None):
        error(str(exception))
        return super().exceptionHandler(exception, protocolName=protocolName)
        

with open('secrets.json', 'r') as f:
    secrets = json.load(f)
    if 'webhooks' in secrets:
        DISCORD_WEBHOOK_URLS = secrets['webhooks']
    else:
        warning('No webhook found in secrets.json')