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
        # self.value = 'A{4} > 1000'  # 验证失败
        # self.value = '(A{0} - Hex2Dec(Max(B[3])))*8 > 1'  # 验证失败
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
        Verify expression when the trigger type is 演算比较
        @pre call when need verify expression
        @post return the result whether verify successful
        @note
        @return result: return the result whether the expression is legal
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

        # 支持A[1], B[1], A(1), B(1)
        reg_item_value = re.compile("([AB])\(\d+\)|([AB])\[\d+\]")
        reg_fun_value = re.compile("(?:MAX|MIN|AVG|HEX2DEC)\(\{0\}\)")

        """
        1   判断表达式AB  是否和PARAM里面的AB一致
        2   判断是否是string表达式
        3   如果是string表达式 则AB必须同为string
        """
        is_string_exp = False
        keys = []
        # 判断表达式是否满足A[1], B[1], A(1), B(1)格式。
        item_list = reg_item_value.findall(value)
        if len(item_list) <= constants.NUMBER_ZERO:
            result = {
                constants.STATUS: constants.FALSE,
                constants.MESSAGE: constants.EXPRESSION_ILLEGAL
            }
            return result
        for item in item_list:
            item = re.search("([AB])", str(item)).group()
            if item not in self.param:
                result = {
                    constants.STATUS: constants.FALSE,
                    constants.MESSAGE: constants.EXPRESSION_A_B_NOT_EXIST,
                }
                return result
            if item not in keys:
                keys.append(item)
            if self.param[item].upper() == "STRING":
                is_string_exp = True
        # 当表达式存在A,B时，判断A,B的类型是否都是String or int
        if len(keys) == constants.NUMBER_TWO and is_string_exp and self.param["A"].upper() != self.param["B"].upper():
            result = {
                constants.STATUS: constants.FALSE,
                constants.MESSAGE: constants.EXPRESSION_A_B_VALUE_TYPE_NOT_SAME,
            }
            return result

        """
        1   分割表达式
        2   如果表达式是STRING 则操作符必须是 == 和 !=
        3   替换function后， 左右表达式的字符只能为
                string表达式: A B ( ) [ ] \s \d \w
                非string表达式: A B \d + - * % ( ) [ ] \s \! \@ \# \$ \& \" \^.
        """
        # 按照 <>|<=|>=|==|!=|<|> 分割表达式， 分为三个部分
        values = re.split(operators, value)
        if len(values) != constants.NUMBER_THREE:
            result = {
                constants.STATUS: constants.FALSE,
                constants.MESSAGE: constants.EXPRESSION_CONDITION_ILLEGAL,
            }
            return result
        # 表达式左面部分
        exp_left = values[0].strip()
        # 表达式条件部分
        exp_operator = values[1].strip()
        # 表达式右面部分
        exp_right = values[2].strip()
        # 判断表达式条件是否在规定条件(<>|<=|>=|==|!=|<|>)里
        if re.search(re.compile(operators), exp_operator) is None or len(exp_operator) >= constants.NUMBER_THREE:
            result = {
                constants.STATUS: constants.FALSE,
                constants.MESSAGE: constants.EXPRESSION_CONDITION_ILLEGAL,
            }
            return result
        # 替换左表达式中的运算符(MAX|MIN|AVG|HEX2DEC)为""
        result_left = reg_function_chars.subn("", exp_left)[0]
        # 替换右表达式中的运算符(MAX|MIN|AVG|HEX2DEC)为""
        result_right = reg_function_chars.subn("", exp_right)[0]
        reg_check = reg_num_chars
        if is_string_exp:
            reg_check = reg_string_chars
        # 左右表达式的运算符替换成""之后，
        # 如果表达式是int类型，且左右表达式存在规定正则[^AB\d\+\-\*/%\(\)\[\]\s\!\@\#\$\&\"\^]以外的字符，视为不合法
        # 如果表达式是String类型，且左右表达式存在规定正则[^AB\(\)\[\]\s\d\w]以外的字符，视为不合法
        if reg_check.search(result_left) is not None or reg_check.search(result_right) is not None:
            msg = ''
            if reg_check.search(result_left) is not None:
                # illegal_left = reg_check.search(result_left).group()
                msg = constants.EXPRESSION_ILLEGAL_IN_LEFT_EXPRESSION % result_left
            if reg_check.search(result_right) is not None:
                # illegal_right = reg_check.search(result_right).group()
                msg = constants.EXPRESSION_ILLEGAL_IN_RIGHT_EXPRESSION % result_right
            result = {
                constants.MESSAGE: msg,
                constants.STATUS: constants.FALSE,
            }
            return result

        """
        1. 将function A B  替换成{0}
        2. 排除\w{0} 的情况
        3.  将{0}  替换成-9999 进行eval 判断
        4.  如果是String类型， 将右表达式  替换成-9999 进行eval 判断
        """
        # 将表达式中的A[1], B[1], A(1), B(1)替换成{0}, return：AVG({0})   MAX({0}) != 1500
        value = reg_item_value.subn("{0}", value)[0]
        # 将表达式中的AVG({0})替换成{0}，return：(u'{0}   {0} != 1500', 2)
        while True:
            result_function = reg_fun_value.subn("{0}", value)
            value = result_function[0]
            if result_function[1] == 0:
                break
        reg_illegal_chars = re.compile("\w\{0\}|\{0\}\w")
        # 此时，如果表达式符合规范，应该为完全替换成{0}， 则不会出现在reg_illegal_chars范围内。
        if reg_illegal_chars.search(value) is not None:
            result = {
                constants.STATUS: constants.FALSE,
                constants.MESSAGE: constants.EXPRESSION_VERIFY_FAILED,
            }
            return result
        # 将{0}替换成-9999， 进行eval运算验证
        value = value.replace("{0}", "-9999")
        # 如果表达式是String类型，则应该把右表达式也同时替换成-9999，否则eval会验证失败
        if is_string_exp:
            value = re.compile("\w+").subn("-9999", value)[0]
        try:
            eval(value)
        except Exception, e:
            result = {
                constants.MESSAGE: constants.EXPRESSION_EVAL_VERIFY_FAILED % (initial_expression, e),
                constants.STATUS: constants.FALSE,
            }
            return result

        result = {
            constants.MESSAGE: constants.SUCCESS,
            constants.STATUS: constants.TRUE,
        }
        return result

    def get(self):
        """!@brief
            Rest Api of GET, verify the expression
            @return data: the status of whether verify successful
            """
        try:
            data = self.expression_verify()
            if data[constants.STATUS] is not 'False':
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
    exp_v = ExpressionVerify('')
    print exp_v.expression_verify()
