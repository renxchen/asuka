from backend.apolo.tools.views_helper import api_return
import simplejson as json
from backend.apolo.tools import constants

import logging
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
formatter = Formatter(
    fmt='%(asctime)s - %(name)s - %(levelname)s - %(thread)d - %(filename)s - %(threadName)s - %(funcName)s - %(message)s',
    datefmt='%Y/%m/%d %p %I:%M:%S')
file_handler = TimedRotatingFileHandler(constants.LOG_PATH, when="D", interval=1, backupCount=5)
file_handler.level = logging.INFO
file_handler.formatter = formatter
logger.addHandler(file_handler)


def exception_handler(e):
    if 'KeyError' in repr(e):
        logger.info("Failed, KeyError occurred")  ###Logger###
        data = {'message': constants.KEY_ERROR % e}
        return api_return(data=eval(json.dumps(data)))
    elif 'PageNotAnInteger' in repr(e):
        logger.info("That page number is not an integer")  ###Logger###
        data = {'message': constants.PAGE_NOT_INTEGER}
        return api_return(data=eval(json.dumps(data)))
    elif 'EmptyPage' in repr(e):
        logger.info("That page number is less than 1")  ###Logger###
        data = {'message': constants.EMPTY_PAGE}
        return api_return(data=eval(json.dumps(data)))
    elif 'IndexError' in repr(e):
        logger.info("List index out of range")  ###Logger###
        data = {'message': "List index out of range"}
        return api_return(data=eval(json.dumps(data)))
    elif 'ValueError' in repr(e):
        logger.info("Parameter type error.")  ###Logger###
        data = {'message': "Parameter type error."}
        return api_return(data=eval(json.dumps(data)))
    elif 'ValidationError' in repr(e):
        logger.info("ValidationError error when execute serializer.is_valid().")  ###Logger###
        data = {'message': str(e)}
        return api_return(data=eval(json.dumps(data)))
    elif 'DoesNotExist' in repr(e):
        logger.info("DoesNotExist error when execute db query.")  ###Logger###
        data = {'message': str(e)}
        return api_return(data=eval(json.dumps(data)))
    elif 'AttributeError' in repr(e):
        logger.info("AttributeError error when execute db query.")  ###Logger###
        data = {'message': str(e)}
        return api_return(data=eval(json.dumps(data)))
    elif 'MultipleObjectsReturned' in repr(e):
        logger.info("MultipleObjectsReturned error when execute db query.")  ###Logger###
        data = {'message': str(e)}
        return api_return(data=eval(json.dumps(data)))
    else:
        logger.info("Error or exception occurred. %s" % str(e))  ###Logger###
        data = {'message': "Error or exception occurred."}
        return api_return(data=eval(json.dumps(data)))
