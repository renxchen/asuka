# -*- coding: utf-8 -*-
import sys
sys.path.append("/Users/yihli/Desktop/projects/apolo")
import time
import copy
from apolo_server.processor.constants import DevicesConstants, CommonConstants, ParserConstants
from apolo_server.processor.db_units.memcached_helper import RulesMemCacheDb, ItemMemCacheDb
from apolo_server.processor.db_units.db_helper import DeviceDbHelp, ItemsDbHelp
from apolo_server.processor.parser.common_policy_tree.tool import Tool


__version__ = '0.1'
__author__ = 'Rubick <haonchen@cisco.com>'


def get_devices(now_time, item_type):
    """
    get Valid items by now time
    """
    device_dict = {}
    devices = []
    
    item_type = CommonConstants.CLI_TYPE_CODE if item_type.upper() == "CLI" \
        else CommonConstants.SNMP_TYPE_CODE
    
    # cache Rules
    rule_dict = {}
    rules = DeviceDbHelp.get_all_rule()
    ruletool = Tool()
    for rule in rules:
        format_rule = ruletool.get_rule_value(rule)
        rule_dict[str(rule['ruleid'])] = format_rule
    
    
    # get items from db 
    items = DeviceDbHelp.get_items(item_type)

    items = get_valid_items(now_time, items)
    #items = [item for item in items if item.get('valid_status')]
    #items = __create_test_devices(items)
    #ItemsDbHelp().update_last_exec_time(now_time, items)

    #tmp_devices = {}
    for item in items:
        # store deviceinfo
        device_id = str(item['device__device_id'])
        if device_id in devices:
            deviceinfo_dict = device_dict[device_id]
        else:
            devices.append(device_id)
            deviceinfo_dict = device_dict[device_id] = {}

        #format data
        if item_type == CommonConstants.CLI_TYPE_CODE:
            __merge_cli(item,deviceinfo_dict,rule_dict) 
        else:
            __merge_snmp(item,deviceinfo_dict) 

    return devices,device_dict


def __create_test_devices(template):
    test_devices = []
    for i in range(68):
        for k in range(101, 116):
            tmp = copy.copy(template[0])
            tmp['device__ip'] = "192.168.100.%d" % k
            tmp['device__device_id'] = i*15 + k
            test_devices.append(tmp)
    return test_devices


def deco_item(func):
    def wrapper(item, now_time):
       
        if item['valid_status'] is False:
            return item
        status = func(item, now_time)
        item['valid_status'] = status
        return item
    return wrapper

def get_items(item_type):

    items = DeviceDbHelp.get_items(item_type)
    return items

def get_valid_items(now_time, items):
    """
       filter by item interval
       combine each item with now_time stamp
       """
    
    item_prioriy_dict = {}
    valid_items = []

    for item in items:    
        item["valid_status"] = True

        __check_item_interval(item, now_time)
        __check_period_time(item, now_time)
        __check_schedule_time(item, now_time)
        __check_device_priority(item,item_prioriy_dict)
       
    for item in items:

        """
            set device's priority status
        """
        priority_key = "%d_%d" % (item["coll_policy_id"], item["device__device_id"])
        if item["valid_status"]:
            if priority_key in item_prioriy_dict and item["schedule__priority"] < item_prioriy_dict[priority_key]["max_priority"]: 
                
                item["valid_status"] = False
        
            """
            filter stop collection
            """
            __check_is_stop_collection(item, now_time)
        
        if item["valid_status"]:
            valid_items.append(item)
        
    return valid_items

def __merge_snmp(item, deviceinfo_dict):

    interval_key_dict={
  
        str(24*60*60):"items_1day",
        str(60*60):"items_1hour",
        str(15*60):"items_15min",
        str(5*60):"items_5min",
        str(60):"items_1min"
    }

    if str(item['device__device_id']) not in deviceinfo_dict:

        deviceinfo_dict['device_id'] = str(item['device__device_id'])
        deviceinfo_dict['ip'] = item['device__ip']
        deviceinfo_dict['hostname'] = item['device__hostname']
        deviceinfo_dict['community'] = item['device__snmp_community']

        """
        deviceinfo_dict['ip'] = "10.71.244.135"
        deviceinfo_dict['hostname'] = "crs1000_1"
        deviceinfo_dict['community'] = "cisco"
        """

        
        deviceinfo_dict['timeout'] = item['device__ostype__snmp_timeout']

    exec_interval=item['policys_groups__exec_interval']
    oid=item['coll_policy__snmp_oid'],
    

    item_key = interval_key_dict[str(exec_interval)]

    if item_key not in deviceinfo_dict:
        deviceinfo_dict[item_key] = []

    deviceinfo_dict[item_key].append( dict(
            item_id=item['item_id'],
            policy_id=item['coll_policy_id'],
            oid=item['coll_policy__snmp_oid'],
            value_type=item['value_type'],
            policy_type=item['item_type']
        )
    )


def __merge_cli(item, deviceinfo_dict,rule_dict):

    interval_key_dict={
        str(24*60*60):"items_1day",
        str(60*60):"items_1hour",
        str(15*60):"items_15min",
        str(5*60):"items_5min",
        str(5*60):"items_1min"
    }

    if str(item['device__device_id']) not in deviceinfo_dict:

        deviceinfo_dict['device_id'] = str(item['device__device_id'])
        deviceinfo_dict['ip'] = item['device__ip']
        deviceinfo_dict['hostname'] = item['device__hostname']
        deviceinfo_dict['expect'] = item['device__login_expect']
        
        #deviceinfo_dict['ip'] = "10.71.244.135"
        #deviceinfo_dict['hostname'] = "crs1000_1"
        #deviceinfo_dict['expect'] = "ssword:,cisco,>,enable,:,cisco123,#"

        deviceinfo_dict['default_commands'] = item['device__ostype__start_default_commands']
        deviceinfo_dict['timeout'] = item['device__ostype__telnet_timeout']
        deviceinfo_dict['method'] = DevicesConstants.CLI_COLLECTION_DEFAULT_METHOD

    
    #exec_interval=item['policys_groups__exec_interval']
    exec_interval=300
    command=item['coll_policy__cli_command']
    #print command
    
    #cmd_key = interval_key_dict[str(exec_interval)][0]
    item_key = interval_key_dict[str(exec_interval)]
    #if command not in deviceinfo_dict[cmd_key]:
        #deviceinfo_dict[cmd_key].append(command)
    
    if item_key not in deviceinfo_dict:
        deviceinfo_dict[item_key] = []

    """
    get rules
    """
    tree_path=item['coll_policy_rule_tree_treeid__rule_id_path']
    rule_id=item['coll_policy_rule_tree_treeid__rule_id']
    rule_path = __split_path(tree_path,rule_id)

    rules = {}
    for ruleid in rule_path:
        rules[ruleid] = rule_dict[ruleid]

    deviceinfo_dict[item_key].append( dict(
            item_id=item['item_id'],
            policy_id=item['coll_policy_id'],
            rule_path=rule_path,
            rules=rules,
            rule_id=item['coll_policy_rule_tree_treeid__rule_id'],
            value_type=item['value_type'],
            policy_type=item['item_type'],
            command=item['coll_policy__cli_command'],
            exec_interval=item['policys_groups__exec_interval']
        )
    )

def __split_path(path, rule_id):
    rules = []
    if len(path) == 1:
        rules.append(str(rule_id))
    else:
        rules = path.split(ParserConstants.TREE_PATH_SPLIT)[1:]
        rules.append(str(rule_id))
    return rules

@deco_item
def __check_item_interval(item, now_time):
    """
    :param item: item instance include:policys_groups__exec_interval, last_exec_time
    :param now_time: now timestampe
    :return:True or False
    """
    exec_interval = item["policys_groups__exec_interval"]
    last_exec_time = item['last_exec_time'] if item['last_exec_time'] is not None  else 0
    # if now_time - last_exec_time >= exec_interval:
    #     return True
    # else:
    #     return False
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
    if item['schedule__valid_period_type'] == DevicesConstants.OPEN_VALID_PERIOD_TYPE:
        item_valid_period_time = __translate_valid_period_date((item['schedule__start_period_time'],
                                                                item['schedule__end_period_time']))
        return __check_date_range(item_valid_period_time[0], item_valid_period_time[1], now_time)
    else:
        return True


@deco_item
def __check_schedule_time(item, now_time):
    """
    Judging given item whether start at now time
    :now_time: given time stamp
    :return:True Or False
    """
    if item["schedule__data_schedule_type"] not in [DevicesConstants.SCHEDULE_GET_NORMALLY,
                                                    DevicesConstants.SCHEDULE_SPECIALLY]:
        return True
    """
    collection data normally
    """
    if item["schedule__data_schedule_type"] == DevicesConstants.SCHEDULE_GET_NORMALLY:
        return True
    # """
    # stop collection data
    # """
    # if item["schedule__data_schedule_type"] == 1:
    #     return False
    """
    collection data periodically
    """
    if item["schedule__data_schedule_type"] == DevicesConstants.SCHEDULE_SPECIALLY:
        """
        filter week
        """
        weeks = str(item["schedule__data_schedule_time"].split(DevicesConstants.SCHEDULE_DATE_SPLIT)[0]).split(
            DevicesConstants.SCHEDULE_WEEKS_SPLIT)
        week_status = __check_week(now_time, weeks)
        if week_status:
            now_date = time.localtime(now_time)
            tmp_start = time.strptime(str(item["schedule__data_schedule_time"].split(
                DevicesConstants.SCHEDULE_DATE_SPLIT)[1])
                                      .split(DevicesConstants.SCHEDULE_SPLIT)[0], "%H:%M")
            tmp_end = time.strptime(str(item["schedule__data_schedule_time"]
                                        .split(DevicesConstants.SCHEDULE_DATE_SPLIT)[1]).split("-")[1], "%H:%M")
            now = time.strptime(str(str(now_date.tm_hour) + ":" + str(now_date.tm_min)), "%H:%M")
            status = __check_date_range(tmp_start, tmp_end, now)
            return status
        return False


def __check_device_priority(item,item_prioriy_dict):
    result = {}
    """
    check priority
    """
   
    if "valid_status" in item.keys() and item['valid_status']:

        item_key = "%d_%d" % (item["coll_policy_id"], item["device__device_id"])

        if item_key in item_prioriy_dict:
            tmp_p_item = item_prioriy_dict[item_key]
            if item["schedule__priority"] > tmp_p_item["max_priority"]:
                item_prioriy_dict.update(item_key,{"max_priority":item["schedule__priority"]})
        else:
            item_prioriy_dict[item_key] = {"max_priority":item["schedule__priority"]}   


@deco_item
def __check_is_stop_collection(item, now_time):
    if item["schedule__data_schedule_type"] == DevicesConstants.SCHEDULE_CLOSED:
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
    start_time_stamp = time.strptime(start_date, DevicesConstants.VALID_DATE_FORMAT)
    end_time_stamp = time.strptime(end_date, DevicesConstants.VALID_DATE_FORMAT)
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
    path_list = path[1:].split(ParserConstants.TREE_PATH_SPLIT)
    result = ['']
    if len(path) != 1:
        for each_path in path_list:
            each_path_rules = rules[str(each_path)]
            result.append(str(each_path_rules['key_str']))
    else:
        result.append('')
    return "/".join(result)



if __name__ == "__main__":
    
    devices,device_dict = get_devices(int(time.time()), "cli")
    #print 123
    print devices
    print device_dict

