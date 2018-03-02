# encoding=utf-8
"""

@author: kimli
@contact: kimli@cisco.com
@file: verify_expression.py
@time: 2018/1/3 17:34
@desc:

"""
import re


def expression_verify(value, param):
    value = value.upper()

    operators = "(<=|>=|==|!=|>|<)"

    reg_num_chars = re.compile("[^AB\d\+\-\*/%\(\)\[\]\s]")
    reg_string_chars = re.compile("[^AB\(\)\[\]\s]")
    reg_function_chars = re.compile("MAX|MIN|AVG|HEX2DEC")

    reg_item_value = re.compile("([AB])\(\d+\)|([AB])\[\d+\]")
    reg_fun_value = re.compile("(?:MAX|MIN|AVG|HEX2DEC)\(\{0\}\)")

    """
    1   判断表达式AB  是否和PARAM里面的AB一致
    2   判断是否是string表达式
    3   如果是string表达式 则AB必须同为string
    """
    is_string_exp = False
    keys = []
    item_list = reg_item_value.findall(value)
    for item in item_list:
        item = re.search("([AB])", item).group()

        if item not in param:
            return False
        if item not in keys:
            keys.append(item)

        if param[item] == "STRING":
            is_string_exp = True

    if len(keys) == 2 and is_string_exp and param["A"] != param["B"]:
        return False

    """
    1   分割表达式
    2   如果表达式是STRING 则操作符必须是 == 和 !=
    3   替换function后， 左右表达式的字符只能为
            string表达式: A B ( ) [ ] \s
            非string表达式: A B \d + - * % ( ) [ ] \s
    """
    values = re.split(operators, value)

    if len(values) != 3:
        return False
    exp_left = values[0].strip()
    exp_operator = values[1].strip()
    exp_right = values[2].strip()

    if is_string_exp and (exp_operator != "!=" or exp_operator != "=="):
        return False

    result_left = reg_function_chars.subn("", exp_left)[0]
    result_right = reg_function_chars.subn("", exp_right)[0]

    reg_check = reg_num_chars
    if is_string_exp:
        reg_check = reg_string_chars
    if reg_check.search(result_left) is not None or reg_check.search(result_right) is not None:
        return False

    """
    1. 将function A B  替换成{0}
    2. 排除\w{0} 的情况
    3  将{0}  替换成-9999 进行eval 判断
    """

    value = reg_item_value.subn("{0}", value)[0]

    while (True):
        result_function = reg_fun_value.subn("{0}", value)
        value = result_function[0]
        if result_function[1] == 0:
            break

    reg_illegal_chars = re.compile("\w\{0\}|\{0\}\w")
    if reg_illegal_chars.search(value) is not None:
        return False

    value = value.replace("{0}", "-9999")
    try:
        eval(value)
    except:
        return False

    return True


if __name__ == "__main__":
    # a = "({0} - Hex2Dec(MAX(B[3])))*8 > 1"

    # print expression_verify(a,{"A":"STRING","B":"INT"})
    # reg_chars = re.compile("[^AB\d\+\-\*/%\(\)\[\]]")
    # print eval("3 != 3 !=4")
    # reg_item_value = re.compile("[AB]\(\d+\)|[AB]\[\d+\]")
    # lista = reg_item_value.findall(a)
    # print re.search("([AB])", lista[0]).group()

    # -9999 - -9999 > 3

    print eval("3-4>-5")
