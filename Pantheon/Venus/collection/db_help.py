import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Pantheon.Venus.db_units.settings")
django.setup()
from ..db_units.models import Items, PolicysGroups


def get_items_schedule(item_type):
    items = Items.objects.filter(**{"status": 1, "schedule__status": 1, "item_type": item_type}).order_by("schedule__priority").values(
        "item_id",
        "schedule__valid_period_type",
        "schedule__valid_period_time",
        "schedule__data_schedule_type",
        "schedule__data_schedule_time",
        "last_exec_time",

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

        "coll_policy__cli_command",
        "coll_policy__snmp_oid",
        # "exec_interval",

        "schedule__priority",
        "policys_groups__exec_interval",
        "policys_groups__history",
        "coll_policy_id",
        "item_type")
    return items


def get_policy_interval(policy_group_id):
    return PolicysGroups.objects.filter(**{"policy_group_id": policy_group_id})[0]

# def update_exec_time():


if __name__ == "__main__":
    # get_items_schedule()
    print get_items_schedule(0)
