from apolo_server.processor.constants import TriggerConstants
import re


class FunctionException(Exception):
    def __init__(self, msg):
        self.msg = msg
        pass

    def __str__(self):
        return self.msg


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

    def _do_get(self, item_id, times=10):
        # TODO: add Max function
        pass


class Min(FunctionBase):
    def __init__(self):
        super(Min, self).__init__()

    def _do_get(self, item_id, times=10):
        # TODO: add Min function
        pass


class Ave(FunctionBase):

    def __init__(self):
        super(Ave, self).__init__()

    def _do_get(self, item_id, times=10):
        # TODO: add Ave function
        pass


class Hex2Dec(FunctionBase):
    def __init__(self):
        super(Hex2Dec, self).__init__()

    def _do_get(self, number):
        try:
            return int(number, 16)
        except Exception, e:
            raise FunctionException("Hex2Dec has error param")


class Last(FunctionBase):
    def __init__(self):
        super(Last, self).__init__()

    def _do_get(self, item_id,  num):
        # TODO: add Last function
        pass


def parser_expression(expression):
    return_str_pattern = "LAST(%s, %s)"
    last_pattern = "(\d+)\((\d+)\)"
    result = re.search(last_pattern, expression)
    return_str = ""
    if result:
        item_id = result.groups()[0]
        num = result.groups()[1]
        return return_str_pattern % (item_id, num)
    else:
        raise FunctionException("Last Function format error")


def handle_expression(expression):
    expression = parser_expression(expression)
    # function_mapping =
    MAX = Max()
    MIN = Min()
    AVE = Ave()
    HEX2DEC = Hex2Dec()
    LAST = Last()
    eval(expression)

if __name__ == "__main__":
    # handle_expression("HEX2DEC(AVE())")
    # print parser_expression("11(10)")
    test = Hex2Dec()
    print test("A10")


