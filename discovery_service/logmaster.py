# From https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output

import logging


class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    green = "\x1b[32;21m"
    grey = "\x1b[0;49;37m"
    green = "\x1b[0;49;32m"
    yellow = "\x1b[0;49;33m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    cyan = "\x1b[0;49;36m"
    magenta = "\x1b[0;49;35m"
    red = "\x1b[0;49;41m"
    blue = "\x1b[0;49;44m"
    cyan = "\x1b[0;49;36m"

    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s)"
    info = "%(asctime)s - %(name)s - {} %(levelname)s {}- {} %(message)s {} (%(filename)s)".format(
        green, reset, grey, reset
    )
    debug = "%(asctime)s - %(name)s - {} %(levelname)s {}- {} %(message)s {} (%(filename)s)".format(
        cyan, reset, grey, reset
    )
    warning = "%(asctime)s - %(name)s - {} %(levelname)s {}- {} %(message)s {} (%(filename)s)".format(
        yellow, reset, grey, reset
    )
    error = "%(asctime)s - %(name)s - {} %(levelname)s {}- {} %(message)s {} (%(filename)s)".format(
        red, reset, grey, reset
    )

    FORMATS = {
        logging.DEBUG: debug,
        logging.INFO: info,
        logging.WARNING: warning,
        logging.ERROR: error,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def logger_obj(app_name, level="DEBUG"):
    # create logger with 'spam_application'
    logger = logging.getLogger(app_name)
    logger.setLevel(level)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    # ch.setLevel("WARNING")

    ch.setFormatter(CustomFormatter())

    logger.addHandler(ch)
    return logger
