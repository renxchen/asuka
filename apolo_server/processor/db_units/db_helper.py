import os
import sys

#from db_units import *
from backend.apolo.models import Items, CollPolicyCliRule, TriggerDetail, Event, CollPolicyGroups
# import models
from apolo_server.processor.constants import CommonConstants, TriggerConstants
from apolo_server.processor.units import TriggerException
import importlib
import time
from django.db import connection
from django.db.utils import OperationalError
from django.forms.models import model_to_dict


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

        cli_items = [
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

        snmp_items = ["device__ostype__snmp_timeout",
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
                "-policys_groups__exec_interval", "schedule__priority").values(*value_items)
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
    @staticmethod
    def snmp_save(data,clock,ns):
        
        value_type = data['value_type']
        table_name = "HistorySnmp%s" % CommonConstants.VALUE_TYPE_MAPPING.get(value_type)
        table = ParserDbHelp.get_history_table(table_name)
        value = data['value']
        item_id = data['item_id']
        
        table.objects.create(value=value,
                    ns=ns,
                    clock=clock,
                    item_id=item_id)



    @staticmethod
    def cli_save(data,clock,ns):
        value_type = data['value_type']
        table_name = "HistoryCli%s" % CommonConstants.VALUE_TYPE_MAPPING.get(value_type)
        table = ParserDbHelp.get_history_table(table_name)
        
        block_path = str(data['block_path'])
        item_id = data['item_id']
        table.objects.create(
                    value=data["value"],
                    ns=ns,
                    clock=clock,
                    item_id=item_id,
                    block_path=block_path)
       

    def bulk_save_result(self, results, clock, item_type):
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
            self.__save_cli_bulk(data, _clock, _ns)
        else:
            self.__save_snmp_bulk(data, _clock, _ns)

    def __save_cli_bulk(self, result, clock, ns):

        for table in result:
            tmp = []
            for data in result[table]:

                block_path = str(data['block_path'])
                item_id = data['item_id']
                tmp.append(table(
                    value=data["value"],
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
                values = data['value']
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
    @staticmethod
    def get_history_table(table_name):
        """
        Search history data from db by given item id and value type
        :param item_id:
        :param policy_type:
        :param value_type:
        :return: history list
        """

        #base_db_format = "History%s%s"
        #table_name = base_db_format % (policy_type, value_type)
        db_module = importlib.import_module(
            TriggerConstants.TRIGGER_DB_MODULES)
        #if hasattr(db_module, table_name) is False:
        #    raise Exception("%s table isn't exist" % table_name)
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
            obj = table.objects.filter(
                **{"item_id": item_id}).order_by("-clock", "-ns").first()
        else:
            objs = table.objects.filter(
                **{"item_id": item_id}).order_by("-clock", "-ns")[:last_param]
            if len(objs) < param:
                raise TriggerException(
                    "History data not exist for last %d" % last_param)
            else:
                obj = objs[last_param - 1]
        return obj

    def get_last_range_value(self, item_id, policy_type, value_type, param):
        table = self.__get_table_module(policy_type, value_type)
        last_param = int(param) + 1
        objs = table.objects.filter(
            **{"item_id": item_id}).order_by("-clock", "-ns")[:last_param]
        if len(objs) < param:
            raise TriggerException(
                "History data not exist for last %d" % last_param)
        return objs

    def get_triggers(self, devices_id):
        triggers = []
        for device_id in devices_id:
            triggers.extend(TriggerDetail.objects.filter(
                **{"device_id": device_id, "status": 1}))
        return triggers

    @staticmethod
    def get_triggerDetail_by_deviceid(device_id):

        return list(TriggerDetail.objects.filter(**{"device_id": device_id, "status": 1}).order_by("-trigger__priority"). \
            values("trigger_id", "expression", "itemA", "itemB","trigger__priority","trigger__trigger_type","trigger__identifier", "trigger__trigger_limit_nums"))

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

    @staticmethod
    def get_latest_event(device_id):

        sql = '''SELECT * FROM event

        JOIN (
            SELECT device_id, trigger_id,max(data_clock) as data_clock
            FROM event where device_id = %d
            GROUP BY device_id,trigger_id
        ) b ON event.device_id = b.device_id and event.trigger_id=b.trigger_id and event.data_clock = b.data_clock and event.device_id = %d
        '''
        event_objs = Event.objects.raw(sql % (int(device_id), int(device_id)))
        return [model_to_dict(_event) for _event in event_objs]


    @staticmethod
    def save_events(events, device_id):
        if events:
            tmp=[]
            for event in events:
                tmp.append(
                    Event(
                        data_clock=event["clock"],
                        number=event["number"],
                        trigger_value=event["trigger_value"],
                        device_id=device_id,
                        trigger_id=event["trigger_id"],
                        triggerd=event["triggerd"],
                        action=event["action"]
                    )
                )
            Event.objects.bulk_create(tmp)

if __name__ == "__main__":


    #event_objs=Event.objects.raw(sql % (1, 1))
    # event_dict = {}
    # for _event in event_objs:

    #    event_dict.setdefault(str(_event.device_id),[]).append(model_to_dict(_event))

    #print [model_to_dict(_event) for _event in event_objs]
    print list(TriggerDetail.objects.filter(**{"device_id": 2042, "status": 1}).order_by("-trigger__priority"). \
            values("trigger_id", "expression", "itemA", "itemB","trigger__priority","trigger__trigger_type","trigger__identifier", "trigger__trigger_limit_nums"))
