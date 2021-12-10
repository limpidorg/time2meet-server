from colorama import Fore, Back, Style, init
import time

from RequestMap.Validators.ValidatorBase import StandardValidator

init()


def log(*args):
    print(Style.DIM, time.time(), '\t', *args, Style.RESET_ALL)


def debug(*args):
    print(Style.DIM, time.time(), '\t', *args, Style.RESET_ALL)


def info(*args):
    print(Style.BRIGHT, time.time(), '\t', *args, Style.RESET_ALL)


def error(*args):
    print(Fore.RED, time.time(), '\t', *args, Style.RESET_ALL)


def fatal(*args):
    print(Fore.RED + Back.WHITE + Style.BRIGHT,
          time.time(), '\t', *args, Style.RESET_ALL)


def warning(*args):
    print(Fore.YELLOW, time.time(), '\t', *args, Style.RESET_ALL)


class Log(StandardValidator):
    def getEvaluationMethod(self, endpoint, protocolName):
        log('Calling', endpoint['endpointIdentifier'],
            'from protocol', protocolName + '.')
        def evaluate():  # Put required/optional arguments here
            return
        return evaluate
