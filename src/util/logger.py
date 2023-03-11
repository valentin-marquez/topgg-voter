import logging
import sys

import colorama


class Formatter(logging.Formatter):
    """
    Logging Formatter to add colors and count warning / errors
    """

    grey = colorama.Fore.LIGHTBLACK_EX
    yellow = colorama.Fore.LIGHTYELLOW_EX
    red = colorama.Fore.LIGHTRED_EX
    bold_red = colorama.Style.BRIGHT + colorama.Fore.RED
    reset = colorama.Style.RESET_ALL

    logging_format = "%(asctime)s %(levelname)s %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + logging_format + reset,
        logging.INFO: colorama.Fore.LIGHTBLUE_EX + logging_format + reset,
        logging.WARNING: yellow + logging_format + reset,
        logging.ERROR: red + logging_format + reset,
        logging.CRITICAL: bold_red + logging_format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# logging.basicConfig(filename='app.log', level=logging.DEBUG,
#                     format='%(asctime)s %(levelname)s %(message)s (%(filename)s:%(lineno)d)')

# logger = logging.getLogger("AUTO VOTER")

logger = logging.getLogger("AUTO VOTER")
logger.propagate = False
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(Formatter())

logger.addHandler(ch)
