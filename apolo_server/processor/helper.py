# -*- coding: utf-8 -*-
# __author__ = 'yihli'

import logging
import os
from constants import SYS_PATH
from logging.handlers import RotatingFileHandler

DEFAULT_LOG_FILE_PATH = os.path.join(SYS_PATH, "logs", "apolo_server.log")

DEFAULT_LOG_LEVEL = logging.DEBUG
#DEFAULT_FILE_LOG_LEVEL = logging.DEBUG



def get_logger(name, level=None):
    if level is None:
        level = DEFAULT_LOG_LEVEL
    log_pattern = '%(asctime)s - %(name)s - %(levelname)s - %(thread)d - %(filename)s - %(threadName)s - %(funcName)s - %(message)s'  
    formatter = logging.Formatter(log_pattern)
    fh = RotatingFileHandler(DEFAULT_LOG_FILE_PATH,
                             maxBytes=10 * 1024 * 1024, backupCount=5)
 
    fh.setLevel(DEFAULT_LOG_LEVEL)

    ch = logging.StreamHandler()
    ch.setLevel(DEFAULT_LOG_LEVEL)

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    logger.addHandler(ch)
    logger.addHandler(fh)
    logger.propagate = False
    return logger
