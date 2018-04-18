# encoding=utf-8
"""

@author: necwang
@contact: necwang@cisco.com
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
        # self.type_a = views_helper.get_request_value(self.request, "type_a", 'GET')
        # self.type_b = views_helper.get_request_value(self.request, 'type_b', 'GET')
        # 通过url传递参数， 需要把 “+” 换成 “%2B”
        self.value = views_helper.get_request_value(self.request, 'value', 'GET')
        # self.type_a = 'string'
        # self.type_b = 'int'
        # self.value = 'A{4} > 1000'  # 验证失败
        # self.value = '(A{0} - Hex2Dec(Max(B[3])))*8 > 1'  # 验证失败
        # self.value = 'Min(4[10]) != 1500'  # 验证失败
        # self.value = 'Hex2Dec(Min(A[10])) > 1500'   Hex2Dec函数不允许套在其他函数外面， 不合法HEX2DEC\((\d+)[\[\(]\d+[\)\]]

        # self.value = 'Hex2Dec(A[10]) != 1500'
        # self.value = '(A[2] - Hex2Dec(Max(B[3])))*8 > 1'
        # self.value = 'Min(A[10]) != 1500'
        # self.value = 'Avg(A[10]) + Max(B[9]) > 1500'
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
        # self.value = 'Avg(A[10]) + Max(B[9]) != Avg(A[10])'
        # self.value = 'Avg(A[10])%2BMax(B[9]) != OK'
        # self.param = {"A": self.type_a, "B": self.type_b}

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

        reg_num_chars = re.compile("[^AB\d\w\+\-\*/%\(\)\[\]\s\!\@\#\$\&\"\^]")

        # reg_string_chars = re.compile("[^AB\(\)\[\]\s\d\w]")
        reg_function_chars = re.compile("MAX|MIN|AVG|HEX2DEC")

        # 支持A[1], B[1], A(1), B(1)
        reg_item_value = re.compile("([AB])\(\d+\)|([AB])\[\d+\]")
        reg_item_addition_value = re.compile("\(d+\)|\[\d+\]")
        reg_fun_value = re.compile("(?:MAX|MIN|AVG|HEX2DEC)\(\{0\}\)")

        # 判断表达式中存在几个[d+]或者(\d+)的格式, [d+]或者(\d+)的数量应该与表达式中AB数量一致，否则校验失败。
        item_addition_list = reg_item_addition_value.findall(value)
        # 判断表达式存在A[1], B[1], A(1), B(1)格式的数量。
        item_list = reg_item_value.findall(value)
        # 只有A或者B的情况
        num = constants.NUMBER_ZERO
        # 若存在[d+], (\d+)数量大于2，表达式中应该有与上述数量相同的AB
        if len(item_addition_list) >= constants.NUMBER_TWO:
            # AB同时存在，或者有多个A,或者多个B的情况
            num = len(item_addition_list)
        # 若表达式的AB数量小于[d+], (\d+)出现的数量， 说明表达式中缺少A或者B，校验失败
        if len(item_list) < num:
            result = {
                constants.STATUS: constants.FALSE,
                constants.MESSAGE: constants.EXPRESSION_ILLEGAL
            }
            return result

        # 按照 <>|<=|>=|==|!=|<|> 分割表达式， 分为左中右三个部分
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
        # 检查左右表达式中是否包含HEX2DEC运算， 如果包含，HEX2DEC必须属于最外层，即Hex2Dec(A[10])形式
        hexadecimal_regexp = re.compile("(?i)HEX2DEC\(([AB])\[\d+\]\)|(?i)HEX2DEC\(([AB])\(\d+\)\)")
        # Hex2Dec(Min(A[10])) > 1500  验证失败
        # Hex2Dec(A[10]) + Hex2Dec(A[10]) > Hex2Dec(Min(A[10]))     验证失败
        # Min(Hex2Dec(A[10])) > 1500   通过
        # Hex2Dec(A[10]) > 1500       通过
        # 左表达式以运算符分割， 分别判断每一块含有HEX2DEC的表达式是否在最外层
        sign = "(\+|\-|\*|\/)"
        exp_left_splited = re.split(sign, exp_left)
        exp_right_splited = re.split(sign, exp_right)
        for i in exp_left_splited:
            if 'HEX2DEC' in i.upper():
                if re.search(hexadecimal_regexp, i.upper()) is None:
                    result = {
                        constants.STATUS: constants.FALSE,
                        constants.MESSAGE: constants.EXPRESSION_HEXADECIMAL_ILLEGAL,
                    }
                    return result
        # 右表达式以运算符分割， 分别判断每一块含有HEX2DEC的表达式是否在最外层
        for i in exp_right_splited:
            if 'HEX2DEC' in i.upper():
                if re.search(hexadecimal_regexp, i.upper()) is None:
                    result = {
                        constants.STATUS: constants.FALSE,
                        constants.MESSAGE: constants.EXPRESSION_HEXADECIMAL_ILLEGAL,
                    }
                    return result
        # 替换左表达式中的运算符(MAX|MIN|AVG|HEX2DEC)为""
        result_left = reg_function_chars.subn("", exp_left)[0]
        # 替换右表达式中的运算符(MAX|MIN|AVG|HEX2DEC)为""
        result_right = reg_function_chars.subn("", exp_right)[0]
        reg_check = reg_num_chars

        """
        1.左右表达式的运算符MAX|MIN|AVG|HEX2DEC, 替换成""之后，
        2.如果左右表达式存在规定正则[^AB\d\w\+\-\*/%\(\)\[\]\s\!\@\#\$\&\"\^]以外的字符，视为不合法
        """
        if reg_check.search(result_left) is not None or reg_check.search(result_right) is not None:
            msg = ''
            if reg_check.search(result_left) is not None:
                # illegal_left = reg_check.search(result_left).group()
                msg = constants.EXPRESSION_ILLEGAL_IN_LEFT_EXPRESSION
            if reg_check.search(result_right) is not None:
                # illegal_right = reg_check.search(result_right).group()
                msg = constants.EXPRESSION_ILLEGAL_IN_LEFT_EXPRESSION
            result = {
                constants.MESSAGE: msg,
                constants.STATUS: constants.FALSE,
            }
            return result
        # 将表达式中的A[1], B[1], A(1), B(1)替换成{0}, 替换后结果为AVG({0})，MAX({0}) != 1500
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
        """
        1.再次确认表达式完全被替换成-9999格式， 防止string表达式存在， 例如：value=Avg(A[10])%2BMax(B[9]) != OK，
        2.目的是将OK替换成-9999
        """
        value = re.compile("\w+").subn("-9999", value)[0]
        try:
            eval(value)
        except Exception, e:
            result = {
                constants.MESSAGE: constants.EXPRESSION_EVAL_VERIFY_FAILED,
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
