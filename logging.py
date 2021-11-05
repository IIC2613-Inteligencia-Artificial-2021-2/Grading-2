from termcolor import colored
from enum import Enum


class LogLevel(Enum):
    INFO = 0
    WARNING = 1
    ERROR = 2

    @staticmethod
    def to_str(level, message):
        if level == LogLevel.INFO:
            return message
        elif level == LogLevel.WARNING:
            return colored(message, "yellow")
        elif level == LogLevel.ERROR:
            return colored(message, "red")

        return colored(message, "magenta")
