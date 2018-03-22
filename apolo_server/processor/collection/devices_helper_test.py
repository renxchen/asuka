# -*- coding: utf-8 -*-
import sys
sys.path.append("/Users/yihli/Desktop/projects/apolo")
import time
import copy
from apolo_server.processor.constants import DevicesConstants, CommonConstants, ParserConstants
from apolo_server.processor.db_units.memcached_helper import RulesMemCacheDb, ItemMemCacheDb
from apolo_server.processor.db_units.db_helper import DeviceDbHelp, ItemsDbHelp



__version__ = '0.1'
__author__ = 'Rubick <haonchen@cisco.com>'


class Valid(object):
    def __init__(self, now_time):
        self.items = get_valid_items(now_time, get_items(CommonConstants.ALL_TYPE_CODE))

    def valid(self, *args, **kwargs):
        pass


class DeviceValid(Valid):
    def __init__(self, now_time):
        super(DeviceValid, self).__init__(now_time)

    def valid(self, device_id):
        devices = [item for item in self.items if item["device__device_id"] == int(device_id)]
        return len(devices)


class PolicyValid(Valid):
    def __init__(self, now_time):
        super(PolicyValid, self).__init__(now_time)

    def valid(self, coll_policy_id):
        devices = [item for item in self.items if item["coll_policy_id"] == int(coll_policy_id)]
        return len(devices)


class PolicyGroupValid(Valid):
    def __init__(self, now_time):
        super(PolicyGroupValid, self).__init__(now_time)

    def valid(self, policys_groups__policy_group_id):
        devices = [item for item in self.items if item["policys_groups__policy_group_id"] == int(policys_groups__policy_group_id)]
        return len(devices)



def get_devices(now_time, item_type):

    device_dict = {}
    devices = []
    
    item_type = CommonConstants.CLI_TYPE_CODE if item_type.upper() == "CLI" \
        else CommonConstants.SNMP_TYPE_CODE
    
    # cache Rulles
    with RulesMemCacheDb() as memcache:
        memcache.cache()
    
    # get items from db 
    #print item_type
    items = DeviceDbHelp.get_items(item_type)
    #print items

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

        #
        if item_type == CommonConstants.CLI_TYPE_CODE:
            __merge_cli(item,deviceinfo_dict) 
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
        tmp_item['device_name'] = item['device__hostname']
        tmp_item['policy_name'] = item['coll_policy__name']
        tmp_item['exec_interval'] = item['policys_groups__exec_interval']
        return tmp_item

    def wrapper_snmp(item):
        return item

    def wrapper_cli(item):
        return item

    result = common(item)
    if item['item_type'] == CommonConstants.CLI_TYPE_CODE:
        result.update(wrapper_cli(result))
    else:
        result.update(wrapper_snmp(result))
    return result


def get_items(item_type):
    # with ItemMemCacheDb() as item:
    #     items = item.update()
    items = DeviceDbHelp.get_items(item_type)
    #items = [item for item in items if __filter_item_type(item, item_type)]
    return items


#def get_valid_items(now_time, item_type):
#    items = get_items(item_type)
#    items = valid_items(now_time, items)
#    items = map(__item_type_mapping, items)
#    return items


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
        #__check_period_time(item, now_time)
        __check_schedule_time(item, now_time)
        __check_device_priority(item,item_prioriy_dict)
       
    for item in items:

        """
            set device's priority status
        """
        priority_key = "%d_%d" % (item["coll_policy_id"], item["device__device_id"])
        if item["valid_status"]:
            if priority_key in item_prioriy_dict and not item_prioriy_dict[priority_key]["valid"]   \
                         and item["item_id"] == item_prioriy_dict[priority_key]["item_id"]:
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
  
        str(24*60*60):["element_1day","items_1day"],
        str(60*60):["element_1hour","items_1hour"],
        str(15*60):["element_15min","items_15min"],
        str(5*60):["element_5min","items_5min"],
        str(60):["element_1min","items_1min"]
    }

    if str(item['device__device_id']) not in deviceinfo_dict:
        #deviceinfo_dict['element_1day']=[]
        #deviceinfo_dict['element_1hour']=[]
        #deviceinfo_dict['element_15min']=[]
        #deviceinfo_dict['element_5min']=[]
        #deviceinfo_dict['element_1min']=[]
        deviceinfo_dict['device_id'] = str(item['device__device_id'])
        deviceinfo_dict['ip'] = item['device__ip']
        deviceinfo_dict['hostname'] = item['device__hostname']
        deviceinfo_dict['community'] = item['device__snmp_community']
        deviceinfo_dict['timeout'] = item['device__ostype__snmp_timeout']
        deviceinfo_dict['items_1day'] = []
        deviceinfo_dict['items_1hour'] = []
        deviceinfo_dict['items_15min'] = []
        deviceinfo_dict['items_5min'] = []
        deviceinfo_dict['items_1min'] = []
       

    exec_interval=item['policys_groups__exec_interval']
    #exec_interval=300
    oid=item['coll_policy__snmp_oid'],
    
    oid_key = interval_key_dict[str(exec_interval)][0]
    item_key = interval_key_dict[str(exec_interval)][1]
    if oid not in deviceinfo_dict[oid_key]:
        deviceinfo_dict[oid_key].append(oid)
        

    deviceinfo_dict[item_key].append( dict(
            item_id=item['item_id'],
            policy_id=item['coll_policy_id'],
            oid=item['coll_policy__snmp_oid'],
            value_type=item['coll_policy__value_type'],
            policy_type=item['item_type']
        )
    )


def __merge_cli(item, deviceinfo_dict):

    interval_key_dict={
        str(24*60*60):["element_1day","items_1day"],
        str(60*60):["element_1hour","items_1hour"],
        str(15*60):["element_15min","items_15min"],
        str(5*60):["element_5min","items_5min"]
        
    }

    if str(item['device__device_id']) not in deviceinfo_dict:
        deviceinfo_dict['element_1day']=[]
        deviceinfo_dict['element_1hour']=[]
        deviceinfo_dict['element_15min']=[]
        deviceinfo_dict['element_5min']=[]
        deviceinfo_dict['device_id'] = str(item['device__device_id'])
        #deviceinfo_dict['ip'] = item['device__ip']
        deviceinfo_dict['ip'] = "10.71.244.135"
        deviceinfo_dict['hostname'] = "crs1000_1"
        deviceinfo_dict['expect'] = "ssword:,cisco,>,enable,:,cisco123,#"
        deviceinfo_dict['default_commands'] = item['device__ostype__start_default_commands']
        deviceinfo_dict['timeout'] = item['device__ostype__telnet_timeout']
        deviceinfo_dict['method'] = DevicesConstants.CLI_COLLECTION_DEFAULT_METHOD
        deviceinfo_dict['items_1day'] = []
        deviceinfo_dict['items_1hour'] = []
        deviceinfo_dict['items_15min'] = []
        deviceinfo_dict['items_5min'] = []
    
    #exec_interval=item['policys_groups__exec_interval']
    exec_interval=300
    command=item['coll_policy__cli_command']
    print command
    
    cmd_key = interval_key_dict[str(exec_interval)][0]
    item_key = interval_key_dict[str(exec_interval)][1]
    if command not in deviceinfo_dict[cmd_key]:
        deviceinfo_dict[cmd_key].append(command)

    deviceinfo_dict[item_key].append( dict(
            item_id=item['item_id'],
            policy_id=item['coll_policy_id'],
            tree_path=item['coll_policy_rule_tree_treeid__rule_id_path'],
            rule_id=item['coll_policy_rule_tree_treeid__rule_id'],
            value_type=item['value_type'],
            policy_type=item['item_type'],
            command=item['coll_policy__cli_command'],
            exec_interval=item['policys_groups__exec_interval']
        )
    )



def __add_param(items, param_keys):
    result = {}
    for key in param_keys:
        if key in items:
            result[key] = items[key]
    return result


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
    elif item_type == CommonConstants.ALL_TYPE_CODE:
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
            if item["schedule__priority"] < tmp_p_item["priority"]:
                item_prioriy_dict.update(item_key,{"item_id":item["item_id"],"priority":item["schedule__priority"],"valid":False})
        else:
            item_prioriy_dict[item_key] = {"item_id":item["item_id"],"priority":item["schedule__priority"],"valid":True}   


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

