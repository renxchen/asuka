from backend.apolo.tools.common import api_return
import simplejson as json
from backend.apolo.tools import constants

import logging
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler
from django.core.paginator import EmptyPage, PageNotAnInteger
import traceback


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
formatter = Formatter(
    fmt='%(asctime)s - %(name)s - %(levelname)s - %(thread)d - %(filename)s - %(threadName)s - %(funcName)s - %(message)s',
    datefmt='%Y/%m/%d %p %I:%M:%S')
file_handler = TimedRotatingFileHandler('apolo/logs/logger_authentication.log', when="D", interval=1, backupCount=5)
file_handler.level = logging.INFO
file_handler.formatter = formatter
logger.addHandler(file_handler)


def exception_handler(e):
    if 'KeyError' in repr(e):
        logger.info("Failed, KeyError occurred")  ###Logger###
        data = {'message': constants.KEY_ERROR % e}
        return api_return(data=eval(json.dumps(data)))
    if 'PageNotAnInteger' in repr(e):
        logger.info("That page number is not an integer")  ###Logger###
        data = {'message': constants.PAGE_NOT_INTEGER}
        return api_return(data=eval(json.dumps(data)))
    if 'EmptyPage' in repr(e):
        logger.info("That page number is less than 1")  ###Logger###
        data = {'message': constants.EMPTY_PAGE}
        return api_return(data=eval(json.dumps(data)))
