__author__ = 'zhutong'

import logging
import os
DEFAULT_LOG_FILE_PATH = os.path.join(os.path.dirname(__file__),"..","logs","server.log")
DEFAULT_LOG_LEVEL = logging.DEBUG
DEFAULT_FILE_LOG_LEVEL = logging.ERROR
from logging.handlers import RotatingFileHandler


def get_logger(name, level=None):
    if level is None:
        level = logging.DEBUG
    log_pattern = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_pattern)
    fh = RotatingFileHandler(DEFAULT_LOG_FILE_PATH, maxBytes=10*1024*1024,backupCount=5)
    #fh = logging.FileHandler(DEFAULT_LOG_FILE_PATH)
    fh.setLevel(DEFAULT_FILE_LOG_LEVEL)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    logger.addHandler(ch)
    logger.addHandler(fh)
    logger.propagate = False
    return logger

