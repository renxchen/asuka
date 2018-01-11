from db_help import get_history
from Pantheon.Venus.constants import VALUE_TYPE_MAPPING, ITEM_TYPE_MAPPING, TRIGGER_BASE_PATH
import importlib


class FunctionException(Exception):
    def __init__(self, message):
        self.__str = message

    def __str__(self):
        return self.__str


class FunctionBase(object):
    def __init__(self):
        pass

    def get_history(self, item):
        return get_history(item.item_id, VALUE_TYPE_MAPPING.get(item.value_type), ITEM_TYPE_MAPPING.get(item.item_type))

    def get_value(self):
        pass


class LastFunction(FunctionBase):
    """
    Last function, get last value according to function param
    :param item:
    :param function_param:
    :return:last(function_param) value
    """
    def __init__(self):
        pass

    def get_value(self, item, param):
        history = self.get_history(item)
        history = history[::-1]
        last_param = int(param)
        if len(history) - 1 < last_param:
            raise FunctionException("History data not exist for last %d" % last_param)
        return history[last_param]


def get_function_value(function):
    """
    :param function: function object
    :return:{function_id: function value}
    """
    function_pattern = "%sFunction"
    function_name = function_pattern % function.function
    function_param = function.parameter
    function_id = function.function_id
    this_module = importlib.import_module(TRIGGER_BASE_PATH + '.function_helper')
    if hasattr(this_module, function_name) is False:
        function_name = function_pattern % "Last"
    function_module = getattr(this_module, function_name)
    instance = function_module()
    return {function_id: instance.get_value(function.item, function_param)}

if __name__ == "__main__":
    pass