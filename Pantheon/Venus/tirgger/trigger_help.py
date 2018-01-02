from db_help import get_functions_by_device_policy, get_latest_event, save_event
from function_help import get_function_value
from Venus.constants import TRIGGER_EVENT_SOURCE, TRIGGER_OPEN, TRIGGER_VALUE, NORMAL_VALUE

import re
import time


def parser(device_id, policy_id):
    """
    Parser trigger which was defined by given device and policy
    :param device_id:
    :param policy_id:
    :return:
    """
    parser_detail = []
    functions = get_functions_by_device_policy(device_id, policy_id)
    functions_value = {}
    """
    Get all of function's value from db
    """
    for function in functions:
        functions_value.update(get_function_value(function))
        parser_detail.append(function.trigger_detail)
    """
    replace trigger expression by function value
    """
    for trigger_detail in parser_detail:
        expression = trigger_detail.expression
        match_words = re.findall("\{(\d+)\}", expression)
        if match_words:
            for word in match_words:
                function_value = functions_value[long(word)].value
                expression = str(expression).replace("{%s}" % word, str(function_value))
        trigger_detail.expression = expression
        trigger_status = 0
        if eval(trigger_detail.expression):
            # print "Error"
            trigger_status = 1
        save_events(trigger_detail.trigger_id, trigger_status)

    # for trigger_detail in parser_detail:
    #     print trigger_detail.expression


def save_events(trigger_id, trigger_status):
    """
    :param trigger_id:
    :param trigger_status: whether trigger
    :return:Null
    """
    """
    trigger_status 0:normal
    trigger_status 1:trigger
    """
    instance = get_latest_event(TRIGGER_EVENT_SOURCE, trigger_id)
    clock = int(time.time())
    if len(instance) == 0:
        latest_number = 0
    else:
        latest_number = instance[len(instance) - 1]['number']

    if trigger_status == TRIGGER_OPEN:
        latest_number = 0
        value = NORMAL_VALUE
    else:
        latest_number += 1
        value = TRIGGER_VALUE

    save_event(TRIGGER_EVENT_SOURCE, trigger_id, latest_number, clock, value)


if __name__ == "__main__":
    parser(1, 1)
    # data = [1, 5, 3, 10, 1, 15]
    # maxs = []
    # for index, value in enumerate(data):
    #     max_value = max(data[0:index+1])
    #     maxs.append(float(max_value - value)/max_value)
    # print max(maxs)
    # s0 = 100
    # w = 1
    # R = [1, 5, 3, 10, 1, 15]
    # for i in R:
    #     s0 = float(s0) / (w * i)
    # print s0
