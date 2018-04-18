#coding=utf-8
from apolo_server.processor.db_units.db_helper import TriggerDbHelp
from apolo_server.processor.units import FunctionException
from apolo_server.processor.constants import TriggerConstants
import re
import time
import logging
import decimal


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

    def _do_get(self, value):
        return value
        #return int(str(number), 16)


class Last(FunctionBase):
    def __init__(self):
        super(Last, self).__init__()

    def _do_get(self, item,  num, trigger_type, hex2dec_ids):
        if num == 0:
            print "asdf"
            value = item["value"]
        else:
            value = TriggerDbHelp().get_last_value(item['item_id'], item['policy_type'], item['value_type'], num).value
        
        if trigger_type in [TriggerConstants.TRIGGER_TYPE_INTEGER_COMPARE,TriggerConstants.TRIGGER_TYPE_EXPRESSION_COMPARE]:
            #re.search()
            if str(item['item_id']) in hex2dec_ids:
                value = int(str(value), 16)
                print "jajaj"
                print value
                print "asdfasdf"
            else:
                value = decimal.Decimal(value)
        else:
            value = str(value)
        return value


class LastRange(FunctionBase):
    def __init__(self):
        super(LastRange, self).__init__()

    def _do_get(self, item, num, trigger_type, hex2dec_ids):
        history = TriggerDbHelp().get_last_range_value(item['item_id'], item['policy_type'], item['value_type'], num)
        values = []

        for h in history:
            value = h.value
            if trigger_type in [TriggerConstants.TRIGGER_TYPE_INTEGER_COMPARE,TriggerConstants.TRIGGER_TYPE_EXPRESSION_COMPARE]:
           
                if str(item['item_id']) in hex2dec_ids:
                    value = int(str(value), 16)
                else:
                    value = decimal.Decimal(value)
            else:
                value = str(value)
            
            values.append(value)
        
        return values


class Fail(FunctionBase):
    def __init__(self):
        super(Fail, self).__init__()

    def _do_get(self, item, num):
        # TODO: add Last function
        pass


def _create_item(item_id, items):
    for item in items:
        if item["item_id"] == item_id:
            #item["tmp_trigger_type"] = _trigger_type
            #if str(item["item_id"]) in hex2dec_ids:
            #    item["tmp_hex2dec"] = True
            return item


    #return items.get(item_id)
    return ""

def parser_expression_last(expression, trigger_type, hex2dec_ids):
    return_str_pattern = "LAST(_create_item(%s, items), %s,%s,%s)"
    last_pattern = "(\d+)\((\d+)\)"
    result = re.search(last_pattern, expression)
    if result:
        item_id = result.groups()[0]
        num = result.groups()[1]
        sub_str = return_str_pattern % (item_id, num, trigger_type, hex2dec_ids)
        expression = re.sub(last_pattern, sub_str, expression)
    return expression


def parser_expression_last_range(expression, trigger_type, hex2dec_ids):
    return_str_pattern = "LASTRANGE(_create_item(%s, items), %s,%s,%s)"
    last_pattern = "(\d+)\[(\d+)\]"
    result = re.search(last_pattern, expression)
    if result:
        item_id = result.groups()[0]
        num = result.groups()[1]
        sub_str = return_str_pattern % (item_id, num, trigger_type, hex2dec_ids)
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


def handle_expression(expression,trigger_type):
    
    expression = expression.upper()
    hex2dec_ids = re.findall("HEX2DEC\((\d+)[\[\(]\d+[\)\]]",expression)
    expression = parser_expression_last(expression,trigger_type,hex2dec_ids)
    expression = parser_expression_last_range(expression,trigger_type,hex2dec_ids)
    #expression = parser_expression_numerical_string(expression)
    return expression


def is_failure_expression(expression, items):
    item_ids = re.findall("(\d+)[\[\(]\d+[\)\]]",expression,re.I)
          
    for item_id in item_ids:
        for item in items:
            if item_id == str(item["item_id"]):

                if item["status"] != "success":
                    return True
                break

    return False
                                




