from db_units import *

from backend.apolo.models import Items, CollPolicyCliRule, TriggerDetail, Event, ActionLog
from backend.apolo import models
from apolo_server.processor.constants import CommonConstants, TriggerConstants
from apolo_server.processor.units import TriggerException
import importlib
import time
import threading
from django.db import connection
from django.db.utils import OperationalError


def is_connection_usable(func):
    def wrapper(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
            # if len(result) > 0:
            #     result[0]
        except OperationalError:
            connection.close()
            result = func(*args, **kwargs)
        return result
    return wrapper


class DbHelp(object):
    def __init__(self):

        pass


class ItemsDbHelp(DbHelp):
    def __init__(self):
        pass

    def update_last_exec_time(self, now_time, items):
        item_ids = []
        for item in items:
            item_ids.append(item['item_id'])

        #for item in items:
        #TODO  may have max in values
        Items.objects.filter(item_id__in = item_ids).update(last_exec_time=now_time)


class DeviceDbHelp(DbHelp):
    def __init__(self):
        pass

    @staticmethod
    def get_items(item_type):
        param_dict = {"policys_groups__status": 1}


        value_items = ["item_id",
                       "schedule__valid_period_type",
                       "schedule__start_period_time",
                       "schedule__end_period_time",
                       "schedule__data_schedule_type",
                       "schedule__data_schedule_time",
                       "last_exec_time",
                       "item_type",
                       "item_id",
                       "device__device_id",
                       "device__ip",
                       "device__hostname",
                       "coll_policy__name",
                       "coll_policy_id",
                       "value_type",
                       "policys_groups__exec_interval",
                       "schedule__priority"
                       ]

        cli_items=[
            "device__ostype__start_default_commands",
            "device__ostype__end_default_commands",
            "device__ostype__log_fail_judges",
            "device__ostype__telnet_prompt",
            "device__ostype__telnet_timeout",
            "device__login_expect",
            "device__telnet_port",
            "coll_policy__cli_command",
            "coll_policy_rule_tree_treeid",
            "coll_policy_rule_tree_treeid__rule_id_path",
            "coll_policy_rule_tree_treeid__rule_id",
            "coll_policy_rule_tree_treeid__rule__value_type"]

        snmp_items=["device__ostype__snmp_timeout",
                    "device__snmp_port",
                    "device__snmp_community",
                    "device__snmp_version",
                    "coll_policy__snmp_oid"]

        if item_type is not None:
            param_dict["item_type"] = item_type
            if item_type == CommonConstants.CLI_TYPE_CODE:
                value_items.extend(cli_items)
            else:
                value_items.extend(snmp_items)
        else:

            value_items.extend(cli_items)
            value_items.extend(snmp_items)



        items = Items.objects.filter(
            **param_dict).order_by(
            "-policys_groups__exec_interval","schedule__priority").values(*value_items)
        return list(items)



    @staticmethod
    def get_all_items_from_db():
        items = Items.objects.filter(
            **{"policys_groups__status": 1, "status": 1, "schedule__status": 1}).order_by(
            "schedule__priority").values(
            "item_id",
            "schedule__valid_period_type",
            "schedule__start_period_time",
            "schedule__end_period_time",
            "schedule__data_schedule_type",
            "schedule__data_schedule_time",
            "last_exec_time",
            "item_type",
            "item_id",
            "device__device_id",
            "device__ip",
            "device__hostname",
            "device__login_expect",
            "device__ostype__start_default_commands",
            "device__ostype__snmp_timeout",
            "device__ostype__telnet_timeout",
            "device__login_expect",
            "device__telnet_port",

            "device__snmp_port",
            "device__snmp_community",
            "device__snmp_version",
            "coll_policy__name",
            "coll_policy__cli_command",
            "coll_policy__snmp_oid",
            # "exec_interval",
            "coll_policy_rule_tree_treeid",
            "coll_policy_rule_tree_treeid__rule_id_path",
            "coll_policy_rule_tree_treeid__rule_id",
            "coll_policy_rule_tree_treeid__rule__value_type",
            "coll_policy__value_type",
            "schedule__priority",
            "policys_groups__exec_interval",
            "policys_groups__history",
            "policys_groups__policy_group_id",
            "policys_groups__policy_group_id__name",
            "coll_policy_id",
            "value_type",
            "coll_policy_id")
        return items

    @staticmethod
    def get_all_rule():
        rules = CollPolicyCliRule.objects.all()
        return rules


class ParserDbHelp(DbHelp):
    def __init__(self):
        pass

    def bulk_save_result(self, results, clock,item_type):
        data = {}
        for result in results:
            value_type = result['value_type']
            keys = self.get_history_table(CommonConstants.VALUE_TYPE_MAPPING.get(value_type),
                                          CommonConstants.ITEM_TYPE_MAPPING.get(item_type))
            if keys in data.keys():
                pass
            else:
                data[keys] = []
            data[keys].append(result)

        clock = float(clock)
        _clock = int(clock)
        _ns = int(str((int(round(clock * 1000))))[-3:])

        if item_type == CommonConstants.CLI_TYPE_CODE:
            self.__save_cli_bulk(data,_clock,_ns)
        else:
            self.__save_snmp_bulk(data,_clock,_ns)



    def __save_cli_bulk(self, result, clock, ns):

        for table in result:
            tmp = []
            for data in result[table]:

                block_path = str(data["data"]['block_path'])
                item_id = data['item_id']
                tmp.append(table(
                    value=data['data']["value"],
                    ns=ns,
                    clock=clock,
                    item_id=item_id,
                    block_path=block_path
                ))

            table.objects.bulk_create(tmp)
        return True

    def __save_snmp_bulk(self, result, clock, ns):


        for table in result:
            tmp = []
            for data in result[table]:
                output = data['value']
                item_id = data['item_id']
                mibs = output.keys()[0]
                value1 = output[mibs][0]
                value2 = output[mibs][1]
                tmp.append(table(
                    value=value1 if value1 else value2,
                    ns=ns,
                    clock=clock,
                    item_id=item_id
                ))
            table.objects.bulk_create(tmp)
        return True

    def get_history_table(self, value_type, policy_type):
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
        return table


class TriggerDbHelp(DbHelp):
    def __init__(self):
        pass

    def __get_table_module(self, policy_type, value_type):
        base_db_format = "History%s%s"
        table_name = base_db_format % (policy_type, value_type)
        # db_module = importlib.import_module(TriggerConstants.TRIGGER_DB_MODULES)
        if hasattr(models, table_name) is False:
            raise Exception("%s table isn't exist" % table_name)
        table = getattr(models, table_name)
        return table

    def get_last_value(self, item_id, policy_type, value_type, param):
        table = self.__get_table_module(policy_type, value_type)
        last_param = int(param) + 1
        if last_param == 1:
            obj = table.objects.filter(**{"item_id": item_id}).order_by("-clock", "-ns").first()
        else:
            objs = table.objects.filter(**{"item_id": item_id}).order_by("-clock", "-ns")[:last_param]
            if len(objs) < param:
                raise TriggerException("History data not exist for last %d" % last_param)
            else:
                obj = objs[last_param - 1]
        return obj

    def get_last_range_value(self, item_id, policy_type, value_type, param):
        table = self.__get_table_module(policy_type, value_type)
        last_param = int(param) + 1
        objs = table.objects.filter(**{"item_id": item_id}).order_by("-clock", "-ns")[:last_param]
        if len(objs) < param:
            raise TriggerException("History data not exist for last %d" % last_param)
        return objs

    def get_triggers(self, devices_id):
        triggers = []
        for device_id in devices_id:
            triggers.extend(TriggerDetail.objects.filter(**{"device_id": device_id, "status": 1}))
        return triggers

    def get_triggers_by_item_id(self, items_id):
        """
        search triggers by different expression pattern
        :param items_id:
        :return:
        """
        value_compare_pattern = "'\\\{%item_id\\\}|" \
                                "%item_id\\\[[0-9]+\\\]|" \
                                "%item_id\\\([0-9]+\\\)|" \
                                "Fail\\\(%item_id\\\)'"
        sql = "SELECT * FROM trigger_detail where expression REGEXP  %s and status=1" % value_compare_pattern
        triggers = []
        for item_id in items_id:
            tmp_sql = sql.replace("%item_id", str(item_id))
            tmp = TriggerDetail.objects.raw(tmp_sql)
            triggers.extend(tmp)
        return triggers

    def get_latest_event(self, source, object_id):
        latest_event = Event.objects.filter(**{"source": source, "objectid": object_id}).order_by('-clock').first()

        return latest_event

    def save_events(self, events):
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


class ActionDbHelp(DbHelp):
    def __init__(self):
        pass

    @staticmethod
    def save_action_log(logs):
        saved_logs = []
        for log in logs:
            saved_logs.append(ActionLog(device_hostname=log['device_hostname'],
                                        action_time=log['action_time'],
                                        action_date=log['action_date'],
                                        coll_policy_name=log['coll_policy_name'],
                                        action_level=log['action_level'],
                                        extra_data=log['extra_data'],
                                        action_status=log['action_status'],
                                        exec_response=log['exec_response'],
                                        action_id=log['action_id'],
                                        exec_action=log['exec_action']
                                        ))
        ActionLog.objects.bulk_create(saved_logs)


def test(id):
    print id
    print list(ActionLog.objects.all())[0].id

if __name__ == "__main__":
    time.clock()
    # TriggerDbHelp.get_last_value(4, "Cli", "Str", 1)
    # print TriggerDbHelp.get_trigger(1)[0].expression
    # print time.clock()
    # instance = CollPolicyGroups()
    # test(1)
    # print '1111'
    # time.sleep(10)
    # test(2)
    # for i in range(100):
    #     t = threading.Thread(target=test, args=(i, ))
    #     t.start()
    # time.sleep(10)
    # t = threading.Thread(target=test, args=(1,))
    # t.start()
    # print 1111
    # time.sleep(5)
    # t = threading.Thread(target=test, args=(2,))
    # t.start()
    # while True:
    #     pass
    #
    # for i in TriggerDbHelp().get_triggers_by_item_id(['4', '1']):
    #     print i
