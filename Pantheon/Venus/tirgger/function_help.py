import importlib
from db_help import get_function_by_id, get_mapping_meaning, get_history


class FunctionException(Exception):
    def __init__(self, message):
        self.__str = message

    def __str__(self):
        return self.__str


def __function_last(item, function_param):
    """
    Last function, get last value according to function param
    :param item:
    :param function_param:
    :return:last(function_param) value
    """
    value_type = get_mapping_meaning("value_type", item.value_type)
    if len(value_type) == 0:
        raise FunctionException("Item id: %d, which value type is not exist in mapping table" % item.item_id)
    policy_type = get_mapping_meaning("policy_type", item.item_type)
    if len(policy_type) == 0:
        raise FunctionException("Item id: %d, which policy type is not exist in mapping table" % item.item_id)
    history = get_history(item.item_id, value_type[0]['code_meaning'], policy_type[0]['code_meaning'])
    history = history[::-1]
    last_param = int(function_param)
    if len(history) - 1 < last_param:
        raise FunctionException("History data not exist for last %d" % last_param)
    return history[last_param]


def __function_default(item, function_param):
    return


def get_function_value(function):
    """
    :param function: function object
    :return:{function_id: function value}
    """
    function_pattern = "__function_%s"
    function_name = function_pattern % function.function
    function_param = function.parameter
    function_id = function.function_id
    this_module = importlib.import_module("function_help")
    if hasattr(this_module, function_name) is False:
        function_name = function_pattern % "default"
    logic_function = getattr(this_module, function_name)
    return {function_id: logic_function(function.item, function_param)}


if __name__ == "__main__":
    get_function_value(get_function_by_id(4))
    # hasattr()
    # print getattr(, "test")