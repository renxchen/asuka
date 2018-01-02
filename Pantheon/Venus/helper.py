__author__ = 'zhutong'

import logging


def get_logger(name, level=None):
    if level is None:
        level = logging.DEBUG
    log_pattern = '[%(asctime)s][%(name)s] %(message)s'
    formatter = logging.Formatter(log_pattern)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(logging.DEBUG)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(ch)
    logger.propagate = False
    return logger

