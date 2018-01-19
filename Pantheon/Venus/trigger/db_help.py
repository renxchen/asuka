import importlib
import time
from Pantheon.Venus.db_units.db_units import *
from Pantheon.Venus.db_units.models import Items, Functions, TriggerDetail, Mapping, Event
from Pantheon.Venus.constants import TriggerConstants


def get_items_by_device_policy(device_id, policy_id):
    """
    :param device_id: device id
    :param policy_id: policy id
    :return: items list
    """
    items = Items.objects.filter(**{"device_id": device_id, "coll_policy_id":  policy_id, "status": 1})
    return items


def get_functions_by_item_id(item_id):
    """
    :param item_id: item id
    :return: functions list
    """
    functions = Functions.objects.filter(**{"item_id": item_id, "item__status": 1})
    return functions


def get_functions_by_device_policy(device_id, policy_id):
    functions = Functions.objects.filter(**{"item__device_id": device_id, "item__coll_policy_id": policy_id,
                                            "item__status": 1})
    return functions


def get_trigger_detail_by_id(trigger_detail_id):
    """
    :param trigger_detail_id:trigger detail's id
    :return: trigger_details list
    """
    trigger_details = TriggerDetail.objects.filter(**{"trigger_detail_id": trigger_detail_id, "status": 1})[0]
    return trigger_details


def get_function_by_id(function_id):
    """
    :param function_id:
    :return:
    """
    function = Functions.objects.filter(**{"function_id": function_id})[0]
    return function


def get_history(item_id, value_type, policy_type):
    """
    Search history data from db by given item id and value type
    :param item_id:
    :param policy_type:
    :param value_type:
    :return: history list
    """

    base_db_format = "History%s%s"
    table_name = base_db_format % (policy_type, value_type)
    db_module = importlib.import_module(TriggerConstants.TRIGGER_DB_MODULES)
    if hasattr(db_module, table_name) is False:
        raise Exception("%s table isn't exist" % table_name)
    table = getattr(db_module, table_name)
    history = table.objects.filter(**{"item_id": item_id}).order_by("clock")
    if value_type not in TriggerConstants.TRIGGER_NUMERIC:
        for h in history:
            h.value = "'" + h.value + "'"
    return history


def get_cli_history(item_id, value_type):
    """
    Search cli history from db
    :param item_id:
    :param value_type:
    :return:
    """
    return get_history(item_id, value_type, "Cli")


def get_snmp_history(item_id, value_type):
    """
    Search snmp history from db
    :param item_id:
    :param value_type:
    :return:
    """
    return get_history(item_id, value_type, "Snmp")


def get_mapping_meaning(source, code):
    code_meaning = Mapping.objects.filter(**{"source": source, "code": code}).values("code_meaning")
    return code_meaning


def get_latest_event(source, object_id):
    latest_event = Event.objects.filter(**{"source": source, "objectid": object_id}).order_by('clock').values("number")
    return latest_event


def save_event(source, object_id, number, clock, value):
    try:
        Event(
            source=source,
            objectid=object_id,
            number=number,
            clock=clock,
            value=value
        ).save()
    except Exception, e:
        raise Exception(e)


def save_events(events):
    tmp = []
    for event in events:
        tmp.append(
            Event(
                source=event[0],
                objectid=event[1],
                number=event[2],
                clock=event[3],
                value=event[4]
            )
        )
    Event.objects.bulk_create(tmp)


if __name__ == "__main__":
    # print get_functions_by_device_policy(1, 1)
    # function = get_functions_by_device_policy(1, 1)
    # for i in function:
    #     print i.trigger_detail.trigger_detail_id
    # pass
    # print get_cli_history(2, "Int")
    # get_trigger_detail_by_policy_device(1, 1)
    time.clock()
    for i in get_history(4, "Str", "Cli"):
        i
        pass
    print time.clock()