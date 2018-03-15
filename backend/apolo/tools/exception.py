from backend.apolo.tools.views_helper import api_return
import simplejson as json
from backend.apolo.tools import constants

import logging
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler
import os
import traceback


def exception_handler(e):
    """!@brief
    Exception handling method, return formatted exception according the type of exception
    @param e: initial exception
    @post return formatted exception
    @return data: return formatted exception
    """
    logger = logging.getLogger("apolo.log")
    if 'KeyError' in repr(e):
        logger.info("Failed, KeyError occurred, detail: %s" % traceback.format_exc(e))
        data = {'message': str(e)}
        return api_return(data=eval(json.dumps(data)))
    elif 'PageNotAnInteger' in repr(e):
        logger.info("That page number is not an integer, detail: %s" % traceback.format_exc(e))
        data = {'message': str(e)}
        return api_return(data=eval(json.dumps(data)))
    elif 'EmptyPage' in repr(e):
        logger.info("That page number is less than 1, detail: %s" % traceback.format_exc(e))
        data = {'message': str(e)}
        return api_return(data=eval(json.dumps(data)))
    elif 'IndexError' in repr(e):
        logger.info("List index out of range, detail: %s" % traceback.format_exc(e))
        data = {'message': str(e)}
        return api_return(data=eval(json.dumps(data)))
    elif 'ValueError' in repr(e):
        logger.info("Parameter type error, detail: %s" % traceback.format_exc(e))
        data = {'message': str(e)}
        return api_return(data=eval(json.dumps(data)))
    elif 'ValidationError' in repr(e):
        logger.info("ValidationError error when execute serializer.is_valid(), detail: %s" % traceback.format_exc(
            e))
        data = {'message': str(e)}
        return api_return(data=eval(json.dumps(data)))
    elif 'DoesNotExist' in repr(e):
        logger.info("DoesNotExist error when execute db query, detail: %s" % traceback.format_exc(e))
        data = {'message': str(e)}
        return api_return(data=eval(json.dumps(data)))
    elif 'AttributeError' in repr(e):
        logger.info("AttributeError error when execute db query, detail: %s" % traceback.format_exc(e))
        data = {'message': str(e)}
        return api_return(data=eval(json.dumps(data)))
    elif 'MultipleObjectsReturned' in repr(e):
        logger.info(
            "MultipleObjectsReturned error when execute db query, detail: %s" % traceback.format_exc(e))
        data = {'message': str(e)}
        return api_return(data=eval(json.dumps(data)))
    elif 'JSONDecodeError' in repr(e):
        logger.info("JSONDecodeError, detail: %s" % traceback.format_exc(e))
        data = {'message': str(e)}
        return api_return(data=eval(json.dumps(data)))
    elif 'OperationalError' in repr(e):
        logger.info("OperationalError, detail: %s" % traceback.format_exc(e))
        data = {'message': str(e)}
        return api_return(data=eval(json.dumps(data)))
    elif 'TypeError' in repr(e):
        logger.info("TypeError, detail: %s" % traceback.format_exc(e))
        data = {'message': str(e)}
        return api_return(data=eval(json.dumps(data)))
    elif 'IOError' in repr(e):
        logger.info("IOError, detail: %s" % traceback.format_exc(e))
        data = {'message': str(e)}
        return api_return(data=eval(json.dumps(data)))
    else:
        logger.info("Error or exception occurred, detail: %s" % traceback.format_exc(e))
        data = {'message': str(e)}
        return api_return(data=eval(json.dumps(data)))
