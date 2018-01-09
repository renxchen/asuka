import time
import re
import copy
from Pantheon.Venus.collection.db_help import get_items_schedule, get_all_rule
from Pantheon.Venus.constants import OPEN_VALID_PERIOD_TYPE, \
    TREE_PATH_SPLIT, \
    VALID_DATE_FORMAT,\
    SCHEDULE_SPECIALLY, SCHEDULE_CLOSED, SCHEDULE_GET_NORMALLY, SCHEDULE_WEEKS_SPLIT, SCHEDULE_DATE_SPLIT, \
    SCHEDULE_SPLIT, CLI_COLLECTION_DEFAULT_METHOD, SNMP_COLLECTION_DEFAULT_METHOD, \
    CLI_TYPE_CODE


def __create_test_devices(template):
    test_devices = []
    for i in range(68):
        for k in range(101, 116):
            tmp = copy.copy(template[0])
            tmp['device__ip'] = "192.168.100.%d" % k
            tmp['device__device_id'] = i*15 + k
            test_devices.append(tmp)
    return test_devices


def get_items(now_time, item_type, other_param=[]):
    items = get_items_schedule(item_type)
    devices = get_task_information(now_time, items)
    devices = __create_test_devices(devices)
    tmp_result = merge_device(devices)
    if item_type == CLI_TYPE_CODE:
        rules = __add_rules()
        devices = [__merge_cli(item, other_param, rules=rules) for item in tmp_result.values()]
    else:
        devices = [__merge_snmp(item, other_param) for item in tmp_result.values()]
        # for device in devices:
        #     device['rules'] = rules
    return devices


def __add_rules():
    tmp_rules = {}
    all_rules = get_all_rule()
    for rule in all_rules:
        tmp_rules[str(rule['ruleid'])] = rule
    return tmp_rules


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


def merge_device(items):
    tmp_devices = {}
    for item in items:
        if item['device__device_id'] in tmp_devices:
            tmp_devices[item['device__device_id']].append(item)
        else:
            tmp_devices[item['device__device_id']] = []
            tmp_devices[item['device__device_id']].append(item)
    return tmp_devices


def get_task_information(now_time, items):
    """
    Get device information which need to be collected at given time
    :param now_time: time stamp
    :return: device information list
    """

    """
    filter by item interval
    combine each item with now_time stamp
    """
    items = map(lambda x: x[0], filter(check_item_interval, map(lambda x: (x, now_time), items)))

    """
    filter by valid period type
    combine each item with now_time stamp
    """
    items = map(lambda x: x[0], filter(check_period_time, map(lambda x: (x, now_time), items)))
    """
    filter by schedule time type
    combine each item with now_time stamp
    """
    items = map(lambda x: x[0], filter(check_schedule_time, map(lambda x: (x, now_time), items)))

    """
    filter device's priority, hard coding
    """
    items = check_device_priority(items)
    """
    filter stop collection
    """
    items = filter(check_is_stop_collection, items)
    return items


def check_device_priority(items):
    result = {}
    """
    Group by policy id and device id
    """
    for item in items:
        item_key = "%s_%s" % (str(item["coll_policy_id"]), str(item["device__device_id"]))
        if item_key in result.keys():
            pass
        else:
            result[item_key] = []
        result[item_key].append(item)
    """
    get biggest priority for each item
    """
    result = map(lambda i: sorted(i, key=lambda x: x['schedule__priority'], reverse=True)[0], result.values())
    return result


def check_item_interval(param):
    item = param[0]
    now_time = param[1]
    exec_interval = item["policys_groups__exec_interval"]
    last_exec_time = item['last_exec_time']
    if now_time / exec_interval == last_exec_time / exec_interval:
        return False
    else:
        return True


def check_period_time(param):
    item = param[0]
    now_time = param[1]
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


def check_is_stop_collection(item):
    if item["schedule__data_schedule_type"] == SCHEDULE_CLOSED:
        return False
    return True


def check_schedule_time(param):
    """
    Judging given item whether start at now time
    :param param:0:item,1:now time
    :return:True Or False
    """
    item = param[0]
    now_time = param[1]
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


if __name__ == "__main__":
    # print int(time.time())
    # get_task_information()
    # print time.localtime()
    # print __translate_valid_period_date("2017-12-12@12:12;2017-12-12@13:12")
    # "2017/12/13 12:12:12 2"
    # "2017/12/15 11:19:44"
    # 1513484916, 1513312116
    # start_time = time.time()
    print get_items(1513312116, 0, ['coll_policy_rule_tree_treeid', 'coll_policy_rule_tree_treeid__rule_id_path', 'item_id'])
    # end_time = time.time()
    # a = 2
    # b = 1 + 1
    # print id(a), id(b)