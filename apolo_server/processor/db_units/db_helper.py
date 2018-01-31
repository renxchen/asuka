from db_units import *
from models import Items, CollPolicyCliRule
from apolo_server.processor.constants import CommonConstants, TriggerConstants
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

    # @staticmethod
    # def get_last_value():
if __name__ == "__main__":
    print DeviceDbHelp.get_all_items_from_db()
