from db_units import *
from models import Items, CollPolicyCliRule, TriggerDetail, Event, CollPolicyGroups
import models
from apolo_server.processor.constants import CommonConstants, TriggerConstants
from apolo_server.processor.units import TriggerException
import importlib
import time


class DbHelp(object):
    def __init__(self):
        pass


class DeviceDbHelp(DbHelp):
    def __init__(self):
        pass

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
        rules = CollPolicyCliRule.objects.filter(**{}).values()
        return rules


class ParserDbHelp(DbHelp):
    def __init__(self):
        pass

    @staticmethod
    def bulk_save_result(results, item_type):
        data = {}
        for result in results:
            value_type = result['value_type']
            keys = ParserDbHelp.get_history_table(CommonConstants.VALUE_TYPE_MAPPING.get(value_type),
                                                  CommonConstants.ITEM_TYPE_MAPPING.get(item_type))
            if keys in data.keys():
                pass
            else:
                data[keys] = []
            data[keys].append(result)
        if item_type == CommonConstants.CLI_TYPE_CODE:
            ParserDbHelp.__save_cli_bulk(data)
        else:
            ParserDbHelp.__save_snmp_bulk(data)

    @staticmethod
    def __save_cli_bulk(result):
        base_time = time.time()
        clock = int(base_time)
        ns = (int(round(base_time * 1000)))
        for table in result:
            tmp = []
            for data in result[table]:
                value = data['value']['extract_data']
                if len(value) == 0:
                    value = None
                block_path = data['block_path']
                item_id = data['item_id']
                tmp.append(table(
                    value=value,
                    ns=clock,
                    clock=data['task_timestamp'],
                    item_id=item_id,
                    block_path=block_path
                ))
            table.objects.bulk_create(tmp)

    @staticmethod
    def __save_snmp_bulk(result):
        base_time = time.time()
        clock = int(base_time)
        ns = (int(round(base_time * 1000)))
        for table in result:
            tmp = []
            for data in result[table]:
                output = data['output']
                item_id = data['item_id']
                mibs = output.keys()[0]
                value1 = output[mibs][0]
                value2 = output[mibs][1]
                tmp.append(table(
                    value=value1 if value1 else value2,
                    ns=clock,
                    clock=data['task_timestamp'],
                    item_id=item_id
                ))
            table.objects.bulk_create(tmp)

    @staticmethod
    def get_history_table(value_type, policy_type):
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

    @staticmethod
    def __get_table_module(policy_type, value_type):
        base_db_format = "History%s%s"
        table_name = base_db_format % (policy_type, value_type)
        # db_module = importlib.import_module(TriggerConstants.TRIGGER_DB_MODULES)
        if hasattr(models, table_name) is False:
            raise Exception("%s table isn't exist" % table_name)
        table = getattr(models, table_name)
        return table

    @staticmethod
    def get_last_value(item_id, policy_type, value_type, param):
        table = TriggerDbHelp.__get_table_module(policy_type, value_type)
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

    @staticmethod
    def get_last_range_value(item_id, policy_type, value_type, param):
        table = TriggerDbHelp.__get_table_module(policy_type, value_type)
        last_param = int(param) + 1
        objs = table.objects.filter(**{"item_id": item_id}).order_by("-clock", "-ns")
        if len(objs) < param:
            raise TriggerException("History data not exist for last %d" % last_param)
        else:
            obj = objs[:last_param]
        return obj

    @staticmethod
    def get_triggers(devices_id):
        triggers = []
        for device_id in devices_id:
            triggers.extend(TriggerDetail.objects.filter(**{"device_id": device_id, "status": 1}))
        return triggers

    @staticmethod
    def get_triggers_by_item_id(items_id):
        """
        search triggers by different expression pattern
        :param items_id:
        :return:
        """
        value_compare_pattern = "'\\\{%item_id\\\}|" \
                                "[%item_id\\\[[0-9]+\\\]|" \
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
    def get_latest_event(source, object_id):
        latest_event = Event.objects.filter(**{"source": source, "objectid": object_id}).order_by('clock').values(
            "number")
        return latest_event

    @staticmethod
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
    time.clock()
    # TriggerDbHelp.get_last_value(4, "Cli", "Str", 1)
    # print TriggerDbHelp.get_trigger(1)[0].expression
    # print time.clock()
    # instance = CollPolicyGroups()
    for i in TriggerDbHelp.get_triggers_by_item_id(['4', '1']):
        print i