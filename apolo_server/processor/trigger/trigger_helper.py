from db_help import get_functions_by_device_policy, get_latest_event, save_events, get_functions_by_item_id
from function_helper import get_function_value
from apolo_server.processor.constants import TriggerConstants
import re
import time


def bulk_trigger(items, clock):
    for item in items:
        trigger(item['item_id'], clock)


def trigger(item_id, clock):
    """
    Parser trigger which was defined by given device and policy
    :param item_id:
    :param clock:
    :return:
    """
    parser_detail = []
    # functions = get_functions_by_device_policy(device_id, policy_id)
    functions = get_functions_by_item_id(item_id)
    functions_value = {}
    events = []
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
        if judging_expression(trigger_detail.expression):
            trigger_status = 1
        events.append([trigger_detail.trigger, trigger_status, clock])
    save_event(events)


def judging_expression(expression):
    return eval(expression)


def save_event(events):
    """
    :param events:
    :return:Null
    """
    """
    trigger_status 0:normal
    trigger_status 1:trigger
    """
    tmp = []
    for event in events:
        trigger_instance = event[0]
        instance = get_latest_event(TriggerConstants.TRIGGER_EVENT_SOURCE, trigger_instance.trigger_id)
        clock = event[2]
        if len(instance) == 0:
            latest_number = 0
        else:
            latest_number = instance[len(instance) - 1]['number']

        if event[1] == TriggerConstants.TRIGGER_OPEN:
            latest_number = 0
            value = TriggerConstants.NORMAL_VALUE
        else:
            latest_number += 1
            value = TriggerConstants.TRIGGER_VALUE
        if latest_number >= trigger_instance.trigger_limit_nums:
            latest_number = 0
        tmp.append([TriggerConstants.TRIGGER_EVENT_SOURCE, trigger_instance.trigger_id, latest_number, event[2], value])
    save_events(tmp)

if __name__ == "__main__":
    import cProfile
    time.clock()
    test = [{"item_id": 4}]
    bulk_trigger(test, 123)
    print time.clock()
    # cProfile.run("bulk_trigger(test, 123)")
    # print eval("None > 1")