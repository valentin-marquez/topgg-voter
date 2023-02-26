import logging

import colorama


class Formatter(logging.Formatter):
    grey = colorama.Fore.LIGHTBLACK_EX
    yellow = colorama.Fore.LIGHTYELLOW_EX
    red = colorama.Fore.LIGHTRED_EX
    bold_red = colorama.Style.BRIGHT + colorama.Fore.RED
    reset = colorama.Style.RESET_ALL

    format = "%(asctime)s %(levelname)s %(message)s (%(filename)s:%(lineno)d)"


    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: colorama.Fore.LIGHTBLUE_EX + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
        
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger("AUTO VOTER")
logger.propagate = False
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(Formatter())

logger.addHandler(ch)