import logging
from logging.handlers import TimedRotatingFileHandler
import pathlib
import sys

PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent.parent

FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s —"
    "%(funcName)s:%(lineno)d — %(message)s")
LOG_DIR = PACKAGE_ROOT / 'logs'
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / 'flask_api.log'



def _get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def _get_file_handler(level=logging.WARNING):
    file_handler = TimedRotatingFileHandler(
                    LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    file_handler.setLevel(level)
    return file_handler


def get_logger(logger_name, level=logging.INFO):

    logger = logging.getLogger(logger_name)

    logger.setLevel(level)

    logger.addHandler(_get_console_handler())
    logger.addHandler(_get_file_handler(level=level))
    logger.propagate = False

    return logger


