import time
import re
import copy
from Pantheon.Venus.collection.db_help import get_items_schedule, get_all_rule, get_all_items_from_db
from Pantheon.Venus.constants import OPEN_VALID_PERIOD_TYPE, \
    TREE_PATH_SPLIT, \
    VALID_DATE_FORMAT,\
    SCHEDULE_SPECIALLY, SCHEDULE_CLOSED, SCHEDULE_GET_NORMALLY, SCHEDULE_WEEKS_SPLIT, SCHEDULE_DATE_SPLIT, \
    SCHEDULE_SPLIT, CLI_COLLECTION_DEFAULT_METHOD, SNMP_COLLECTION_DEFAULT_METHOD, \
    CLI_TYPE_CODE, ALL_TYPE_CODE


def deco_item(func):
    def wrapper(item, now_time):
        if "valid_status" in item.keys():
            if item['valid_status'] is False:
                return item
        status = func(item, now_time)
        item = __add_items_valid_status(item, status)
        return item
    return wrapper


def __item_type_mapping(item):
    def common(item):
        tmp_item = {}
        tmp_item['valid_status'] = item['valid_status']
        tmp_item['policy_group_id'] = item['policys_groups__policy_group_id']
        tmp_item['policy_group_name'] = item['policys_groups__policy_group_id__name']
        tmp_item['coll_policy_id'] = item['coll_policy_id']
        tmp_item['item_id'] = item['item_id']
        tmp_item['item_type'] = item['item_type']
        tmp_item['device_id'] = item['device__device_id']
        tmp_item['priority'] = item['schedule__priority']
        return tmp_item

    def wrapper_snmp(item):
        return item

    def wrapper_cli(item):
        return item

    result = common(item)
    if item['item_type'] == CLI_TYPE_CODE:
        result.update(wrapper_cli(result))
    else:
        result.update(wrapper_snmp(result))
    return result


def get_items(now_time, item_type):
    items = get_all_items_from_db()
    items = [item for item in items if __filter_item_type(item, item_type)]
    return items


def get_valid_items(now_time, item_type):
    items = get_items(now_time, item_type)
    items = valid_items(now_time, items)
    items = map(__item_type_mapping, items)
    return items


def valid_items(now_time, items):
    """
       filter by item interval
       combine each item with now_time stamp
       """
    items = [item for item in items if __check_item_interval(item, now_time)]

    """
    filter by valid period type
    combine each item with now_time stamp
    """
    items = [item for item in items if __check_period_time(item, now_time)]
    """
    filter by schedule time type
    combine each item with now_time stamp
    """
    items = [item for item in items if __check_schedule_time(item, now_time)]

    """
    filter device's priority, hard coding
    """
    items = __check_device_priority(items)

    """
    get biggest priority for each item
    """

    """
    filter stop collection
    """
    items = [item for item in items if __check_is_stop_collection(item, now_time)]
    return items


def get_devices(now_time, item_type):
    items = get_items(now_time, item_type)
    items = valid_items(now_time, items)
    items = [item for item in items if item.get('valid_status')]
    devices = __merge_device(items)
    other_param = []
    if item_type == CLI_TYPE_CODE:
        rules = __add_rules()
        devices = [__merge_cli(item, other_param, rules=rules) for item in devices.values()]
    else:
        devices = [__merge_snmp(item, other_param) for item in devices.values()]
    return devices


def __merge_snmp(items, param_keys):
    result = dict()
    if len(items) == 0:
        return []
    result['ip'] = items[0]['device__ip']
    result['community'] = items[0]['device__snmp_community']
    result['timeout'] = items[0]['device__ostype__snmp_timeout']

    result['commands'] = dict(
        operate="",
        oids=[]
    )
    result['items'] = []
    result.update(__add_param(items[0], param_keys))
    for item in items:
        result["commands"]['operate'] = "bulk_get"
        result["commands"]['oids'].append(item['coll_policy__snmp_oid'])
        result['items'].append(
            dict(
                item_id=item['item_id'],
                policy_id=item['coll_policy_id'],
                oid=item['coll_policy__snmp_oid'],
                device_id=item['device__device_id'],
                value_type=item['coll_policy__value_type']
            )

        )
    return result


def __merge_cli(items, param_keys, rules):
    result = dict()
    if len(items) == 0:
        return []
    result['ip'] = items[0]['device__ip']
    result['expect'] = items[0]['device__login_expect']
    result['default_commands'] = items[0]['device__ostype__start_default_commands']
    result['timeout'] = items[0]['device__ostype__telnet_timeout']
    result['commands'] = []
    result['method'] = CLI_COLLECTION_DEFAULT_METHOD
    result['platform'] = 'ios'
    result['rules'] = rules
    result['items'] = []
    result.update(__add_param(items[0], param_keys))
    for item in items:

        result["commands"].append(item['coll_policy__cli_command'])
        result['items'].append(
            dict(
                item_id=item['item_id'],
                policy_id=item['coll_policy_id'],
                tree_id=item['coll_policy_rule_tree_treeid'],
                tree_path=item['coll_policy_rule_tree_treeid__rule_id_path'],
                command=item['coll_policy__cli_command'],
                rule_id=item['coll_policy_rule_tree_treeid__rule_id'],
                device_id=item['device__device_id'],
                value_type=item['coll_policy_rule_tree_treeid__rule__value_type'],
                block_path=__create_path(rules, item['coll_policy_rule_tree_treeid__rule_id_path'])
            )

        )
    return result


def __add_param(items, param_keys):
    result = {}
    for key in param_keys:
        if key in items:
            result[key] = items[key]
    return result


def __add_rules():
    tmp_rules = {}
    all_rules = get_all_rule()
    for rule in all_rules:
        tmp_rules[str(rule['ruleid'])] = rule
    return tmp_rules


def __merge_device(items):
    tmp_devices = {}
    for item in items:
        if item['device__device_id'] in tmp_devices:
            tmp_devices[item['device__device_id']].append(item)
        else:
            tmp_devices[item['device__device_id']] = []
            tmp_devices[item['device__device_id']].append(item)
    return tmp_devices


def __filter_item_type(item, item_type):
    """
    :param item: item Queryset
    :param item_type: 0: cli 1 snmp -1 all
    :return: True or False
    """
    if item['item_type'] == item_type:
        return True
    elif item_type == ALL_TYPE_CODE:
        return True
    else:
        return False


@deco_item
def __check_item_interval(item, now_time):
    """
    :param item: item instance include:policys_groups__exec_interval, last_exec_time
    :param now_time: now timestampe
    :return:True or False
    """
    exec_interval = item["policys_groups__exec_interval"]
    last_exec_time = item['last_exec_time']
    if now_time / exec_interval == last_exec_time / exec_interval:
        return False
    else:
        return True


@deco_item
def __check_period_time(item, now_time):
    """
    0: open valid period type
    1: close valid period type
    """
    if item['schedule__valid_period_type'] == OPEN_VALID_PERIOD_TYPE:
        item_valid_period_time = __translate_valid_period_date((item['schedule__start_period_time'],
                                                                item['schedule__end_period_time']))
        return __check_date_range(item_valid_period_time[0], item_valid_period_time[1], now_time)
    else:
        return True


@deco_item
def __check_schedule_time(item, now_time):
    """
    Judging given item whether start at now time
    :param param:0:item,1:now time
    :return:True Or False
    """
    if item["schedule__data_schedule_type"] not in [SCHEDULE_GET_NORMALLY, SCHEDULE_SPECIALLY]:
        return True
    """
    collection data normally
    """
    if item["schedule__data_schedule_type"] == SCHEDULE_GET_NORMALLY:
        return True
    # """
    # stop collection data
    # """
    # if item["schedule__data_schedule_type"] == 1:
    #     return False
    """
    collection data periodically
    """
    if item["schedule__data_schedule_type"] == SCHEDULE_SPECIALLY:
        """
        filter week
        """
        weeks = str(item["schedule__data_schedule_time"].split(SCHEDULE_DATE_SPLIT)[0]).split(SCHEDULE_WEEKS_SPLIT)
        week_status = __check_week(now_time, weeks)
        if week_status:
            now_date = time.localtime(now_time)
            tmp_start = time.strptime(str(item["schedule__data_schedule_time"].split(SCHEDULE_DATE_SPLIT)[1])
                                      .split(SCHEDULE_SPLIT)[0], "%H:%M")
            tmp_end = time.strptime(str(item["schedule__data_schedule_time"]
                                        .split(SCHEDULE_DATE_SPLIT)[1]).split("-")[1], "%H:%M")
            now = time.strptime(str(str(now_date.tm_hour) + ":" + str(now_date.tm_min)), "%H:%M")
            status = __check_date_range(tmp_start, tmp_end, now)
            return status
        return False


def __check_device_priority(items):
    result = {}
    """
    Group by policy id and device id
    """
    invalid_items = []
    for item in items:
        if "valid_status" in item.keys():
            if item['valid_status'] is False:
                invalid_items.append(item)
                continue
        item_key = "%s_%s" % (str(item["coll_policy_id"]), str(item["device__device_id"]))
        if item_key in result.keys():
            pass
        else:
            result[item_key] = []
        result[item_key].append(item)

    tmp_items = map(lambda i: sorted(i, key=lambda x: x['schedule__priority'], reverse=True), result.values())
    items = []
    status = None
    for tmp in tmp_items:
        for i, value in enumerate(tmp):
            if i == 0:
                status = True
            else:
                status = False
            value['valid_status'] = status
            items.append(value)
    items.extend(invalid_items)
    return items


@deco_item
def __check_is_stop_collection(item, now_time):
    if item["schedule__data_schedule_type"] == SCHEDULE_CLOSED:
        return False
    return True


def __translate_valid_period_date(given_date):
    """
    translate given date to time stamp
    :param given_date: Schedule's valid period time
    :return:time stamp
    """
    start_date = given_date[0]
    end_date = given_date[1]
    start_time_stamp = time.strptime(start_date, VALID_DATE_FORMAT)
    end_time_stamp = time.strptime(end_date, VALID_DATE_FORMAT)
    return int(time.mktime(start_time_stamp)), int(time.mktime(end_time_stamp))


def __check_date_range(start_time, end_time, now_time):
    """
    Judging given time whether in date range
    :param start_time: start date time stamp
    :param end_time: end date time stamp
    :param now_time: now date time stamp
    :return: True or False
    """
    if start_time <= now_time <= end_time:
        return True
    return False


def __check_week(now_time, weeks):
    """
    Judging given now time is given week
    :param now_time: time stamp
    :param weeks:week
    :return:True Or False
    """
    now_date = time.localtime(now_time)
    if str(now_date.tm_wday + 1) in weeks:
        return True
    return False


def __create_path(rules, path):
    path_list = path[1:].split(TREE_PATH_SPLIT)
    result = ['']
    if len(path) != 1:
        for each_path in path_list:
            each_path_rules = rules[str(each_path)]
            result.append(str(each_path_rules['key_str']))
    else:
        result.append('')
    return "/".join(result)


def __add_items_valid_status(item, status):
    item['valid_status'] = status
    return item


if __name__ == "__main__":
    for i in get_valid_items(1513312116, -1):
        print i