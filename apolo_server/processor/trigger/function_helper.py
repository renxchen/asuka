#coding=utf-8
from apolo_server.processor.db_units.db_helper import TriggerDbHelp
from apolo_server.processor.units import FunctionException
import re
import logging


class FunctionBase(object):
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        return self._do_get(*args, **kwargs)

    def _do_get(self, param):
        pass

    def __str__(self):
        return self.__class__.__name__


class Max(FunctionBase):
    def __init__(self):
        super(Max, self).__init__()

    def _do_get(self, values):
        if isinstance(values, list) is False:
            raise FunctionException("Max Function has error param")
        for i in values:
            if isinstance(i, int) or isinstance(i, float) or isinstance(i, long):
                continue
            else:
                raise FunctionException("Max Function has error param")
        return max(values)


class Min(FunctionBase):
    def __init__(self):
        super(Min, self).__init__()

    def _do_get(self, values):
        if isinstance(values, list) is False:
            raise FunctionException("Max Function has error param")
        for i in values:
            if isinstance(i, int) or isinstance(i, float) or isinstance(i, long):
                continue
            else:
                raise FunctionException("Max Function has error param")
        result = min(values)
        return result


class Avg(FunctionBase):
    def __init__(self):
        super(Avg, self).__init__()

    def _do_get(self, values):

        if isinstance(values, list) is False:
            raise FunctionException("Max Function need list param")
        for i in values:
            if isinstance(i, int) or isinstance(i, float) or isinstance(i, long):
                continue
            else:
                raise FunctionException("Max Function has error param")
        return float(sum(values)) / len(values)


class Hex2Dec(FunctionBase):
    def __init__(self):
        super(Hex2Dec, self).__init__()

    def _do_get(self, number):
        return int(number, 16)


class Last(FunctionBase):
    def __init__(self):
        super(Last, self).__init__()

    def _do_get(self, item,  num):
        value = TriggerDbHelp.get_last_value(item['item_id'], item['policy_type'], item['value_type'], num).value
        return value


class LastRange(FunctionBase):
    def __init__(self):
        super(LastRange, self).__init__()

    def _do_get(self, item, num):
        history = TriggerDbHelp.get_last_range_value(item['item_id'], item['policy_type'], item['value_type'], num)
        value = [h.value for h in history]
        return value


class Fail(FunctionBase):
    def __init__(self):
        super(Fail, self).__init__()

    def _do_get(self, item, num):
        # TODO: add Last function
        pass


def _create_item(item_id, items):
    return items.get(item_id)


def parser_expression_last(expression):
    return_str_pattern = "LAST(_create_item(%s, items), %s)"
    last_pattern = "(\d+)\((\d+)\)"
    result = re.search(last_pattern, expression)
    if result:
        item_id = result.groups()[0]
        num = result.groups()[1]
        sub_str = return_str_pattern % (item_id, num)
        expression = re.sub(last_pattern, sub_str, expression)
    return expression


def parser_expression_last_range(expression):
    return_str_pattern = "LASTRANGE(_create_item(%s, items), %s)"
    last_pattern = "(\d+)\[(\d+)\]"
    result = re.search(last_pattern, expression)
    if result:
        item_id = result.groups()[0]
        num = result.groups()[1]
        sub_str = return_str_pattern % (item_id, num)
        expression = re.sub(last_pattern, sub_str, expression)
    return expression


def parser_expression_numerical_string(expression):
    return_str_pattern = "LAST(_create_item(%s, items), 0)"
    last_pattern = "\{(\d+)\}"
    result = re.search(last_pattern, expression)
    if result:
        item_id = result.groups()[0]
        sub_str = return_str_pattern % (item_id, )
        expression = re.sub(last_pattern, sub_str, expression)
    return expression


def handle_expression(expression):
    expression = expression.upper()
    expression = parser_expression_last(expression)
    expression = parser_expression_last_range(expression)
    expression = parser_expression_numerical_string(expression)
    return expression


