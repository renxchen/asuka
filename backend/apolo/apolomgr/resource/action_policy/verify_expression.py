# encoding=utf-8
"""

@author: kimli
@contact: kimli@cisco.com
@file: verify_expression.py
@time: 2018/1/3 17:34
@desc:

"""
import re
import traceback
from backend.apolo.tools.views_helper import api_return
from backend.apolo.tools import constants

from backend.apolo.tools import views_helper
from rest_framework import viewsets
from backend.apolo.tools.exception import exception_handler


class ExpressionVerify(viewsets.ViewSet):
    # class ExpressionVerify(object):
    def __init__(self, request, **kwargs):
        super(ExpressionVerify, self).__init__(**kwargs)
        self.request = request
        self.type_a = views_helper.get_request_value(self.request, "type_a", 'GET')
        self.type_b = views_helper.get_request_value(self.request, 'type_b', 'GET')
        self.value = views_helper.get_request_value(self.request, 'value', 'GET')
        # self.type_a = 'string'
        # self.type_b = 'int'
        # self.value = 'A{4} > 1000'  # 没考虑到的情况(A{0}这种写法好像不允许)
        # self.value = '(A{0} - Hex2Dec(Max(B[3])))*8 > 1'  # 验证失败， 应该通过才对(A{0}这种写法好像不允许)； 并且，如果是除了== !=之外， 必须是string类型才能通过（这个问题可以忽略，因为string和int是前台传过来的)
        # self.value = 'Min(4[10]) != 1500'  # 验证失败
        # self.value = '(A[2] - Hex2Dec(Max(B[3])))*8 > 1'
        # self.value = 'Min(A[10]) != 1500'
        # self.value = 'Avg(A[10]) + Max(B[9]) > 1500'
        # self.value = 'Hex2Dec(Min(A[10])) > 1500'
        # self.value = 'Hex2Dec(Min(A[10])) == 1500'
        # self.value = 'Hex2Dec(Min(A[10])) != 1500'
        # self.value = 'Avg(A[10]) + Max(B[9]) == 1500'
        # self.value = 'A[2] == "$%^*())"'
        # self.value = 'A(4) > 1000'
        # self.value = 'A[4] > 1000'
        # self.value = 'A{4} > 1000'
        # self.value = 'OK != Avg(A[10])'
        # self.value = 'Avg(A(4)) != OK'
        # self.value = 'Avg(A[10]) != 111111'
        # self.value = 'Avg(A[10]) != 111111'
        # self.value = '11OK1 == Avg(A[10]) '
        # self.value = 'Avg(A[10]) + Max(B[9]) != 1500'
        self.param = {"A": self.type_a, "B": self.type_b}

    def expression_verify(self):
        """!@brief
        Verify expression
        @pre call when need the verify expression
        @post return the result whether verify successful
        @note
        @return result: return the result whether verify successful
        """
        initial_expression = self.value
        value = self.value.upper()

        operators = "(<>|<=|>=|==|!=|<|>)"

        #  ^"[^]"$， A{4} == "$%^*())"
        # reg_num_chars = re.compile("[^AB\d\+\-\*/%\(\)\[\]\s]")
        reg_num_chars = re.compile("[^AB\d\+\-\*/%\(\)\[\]\s\!\@\#\$\&\"\^]")
        # (A[10]) + (B[9])
        # AVSSG(A[10]) + (B[9])

        reg_string_chars = re.compile("[^AB\(\)\[\]\s\d\w]")
        reg_function_chars = re.compile("MAX|MIN|AVG|HEX2DEC")

        reg_item_value = re.compile("([AB])\(\d+\)|([AB])\[\d+\]")  # 支持A[1], B[1], A(1), B(1)
        reg_fun_value = re.compile("(?:MAX|MIN|AVG|HEX2DEC)\(\{0\}\)")

        """
        1   判断表达式AB  是否和PARAM里面的AB一致
        2   判断是否是string表达式
        3   如果是string表达式 则AB必须同为string
        """
        is_string_exp = False
        keys = []
        item_list = reg_item_value.findall(value)
        if len(item_list) <= 0:
            result = {
                'msg': 'The expression not support, support expressions: A[1], B[1], A(1), B(1)',
                'status': False,
            }
            return result
        for item in item_list:
            item = re.search("([AB])", str(item)).group()
            if item not in self.param:
                result = {
                    'msg': 'A and B not in expression',
                    'status': False,
                }
                return result
            if item not in keys:
                keys.append(item)
            if self.param[item].upper() == "STRING":
                is_string_exp = True
        if len(keys) == 2 and is_string_exp and self.param["A"].upper() != self.param["B"].upper():
            result = {
                'msg': 'A and B do not have the same type(both of A,B should be str or int)',
                'status': False,
            }
            return result

        """
        1   分割表达式
        2   如果表达式是STRING 则操作符必须是 == 和 !=
        3   替换function后， 左右表达式的字符只能为
                string表达式: A B ( ) [ ] \s \d \w
                非string表达式: A B \d + - * % ( ) [ ] \s \! \@ \# \$ \& \" \^.
        """
        values = re.split(operators, value)
        if len(values) != 3:
            result = {
                'msg': 'The operation condition maybe not in (<=|>=|==|!=|>|<), so can not split as operation condition correctly',
                'status': False,
            }
            return result
        exp_left = values[0].strip()
        exp_operator = values[1].strip()
        exp_right = values[2].strip()
        if re.search(re.compile(operators), exp_operator) is None or len(exp_operator) >= 3:
            result = {
                'msg': 'The operation should be (<=|>=|==|!=|>|<)',
                'status': False,
            }
            return result

        result_left = reg_function_chars.subn("", exp_left)[0]
        result_right = reg_function_chars.subn("", exp_right)[0]
        reg_check = reg_num_chars
        if is_string_exp:
            reg_check = reg_string_chars
        if reg_check.search(result_left) is not None or reg_check.search(result_right) is not None:
            msg = ''
            if reg_check.search(result_left) is not None:
                # illegal_left = reg_check.search(result_left).group()
                msg = 'The expression verify failed, illegal character %s exist in left expression' % result_left
            if reg_check.search(result_right) is not None:
                # illegal_right = reg_check.search(result_right).group()
                msg = 'The expression verify failed, illegal character %s exist in right expression' % result_right
            result = {
                'msg': msg,
                'status': False,
            }
            return result

        """
        1. 将function A B  替换成{0}
        2. 排除\w{0} 的情况
        3.  将{0}  替换成-9999 进行eval 判断
        4.  如果是String类型， 将右表达式  替换成-9999 进行eval 判断
        """
        value = reg_item_value.subn("{0}", value)[0]
        while True:
            result_function = reg_fun_value.subn("{0}", value)
            value = result_function[0]
            if result_function[1] == 0:
                break
        reg_illegal_chars = re.compile("\w\{0\}|\{0\}\w")
        if reg_illegal_chars.search(value) is not None:
            result = {
                'msg': 'The expression verify failed, \w{0} situation exist',
                'status': False,
            }
            return result
        value = value.replace("{0}", "-9999")
        if is_string_exp:
            value = re.compile("\w+").subn("-9999", value)[0]
        try:
            eval(value)
        except Exception, e:
            result = {
                'msg': 'eval verify failed for expression %s, error message: %s' % (initial_expression, e),
                'status': False,
            }
            return result

        result = {
            'msg': 'successful',
            'status': True,
        }
        return result

    def get(self):
        """!@brief
            Rest Api of GET, verify the expression
            @return data: the status
            """
        try:
            data = self.expression_verify()
            if data['status']:
                data = {
                    constants.STATUS: {
                        constants.STATUS: constants.TRUE,
                        constants.MESSAGE: constants.SUCCESS
                    },
                }
                return api_return(data=data)
            else:
                return api_return(data=data)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)


if __name__ == "__main__":
    # Min(A[10]) != 1500 or 1500 != Min(A[10])
    # Hex2Dec(Min(A[10])) > 1500
    # Avg(A[10]) + Max(B[9]) > 1500
    # {4} == "$%^*())"
    # {4} > 1000
    # Fail(1)
    # a = "({0} - Hex2Dec(MAX(B[3])))*8 > 1"
    exp_v = ExpressionVerify('')
    print exp_v.expression_verify()
    # reg_chars = re.compile("[^AB\d\+\-\*/%\(\)\[\]]")
    # print eval("3 != 3 !=4")
    # reg_item_value = re.compile("[AB]\(\d+\)|[AB]\[\d+\]")
    # lista = reg_item_value.findall(a)
    # print re.search("([AB])", lista[0]).group()
