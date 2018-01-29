from db_units import *
from models import Items, CollPolicyCliRule


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
            "item_type",
            "coll_policy_id")
        return items

    @staticmethod
    def get_all_rule():
        rules = CollPolicyCliRule.objects.filter(**{}).values()
        return rules

if __name__ == "__main__":
    print DeviceDbHelp.get_all_items_from_db()
