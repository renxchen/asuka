from Pantheon.Venus.db_units import db_units
from Pantheon.Venus.db_units.models import CollPolicyCliRule
from Pantheon.Venus.constants import TRIGGER_DB_MODULES, VALUE_TYPE_MAPPING, CLI_TYPE_CODE, \
    ITEM_TYPE_MAPPING
import importlib
import time


def get_all_rule():
    rules = CollPolicyCliRule.objects.filter(**{}).values()
    return rules


def bulk_save_result(results, item_type):
    data = {}
    for result in results:
        value_type = result['value_type']
        keys = get_history_table(VALUE_TYPE_MAPPING.get(value_type), ITEM_TYPE_MAPPING.get(item_type))
        if keys in data.keys():
            pass
        else:
            data[keys] = []
        data[keys].append(result)
    if item_type == CLI_TYPE_CODE:
        __save_cli_bulk(data)
    else:
        __save_snmp_bulk(data)


def __save_cli_bulk(result):
    base_time = time.time()
    clock = int(base_time)
    ns = (int(round(base_time * 1000)))
    for table in result:
        tmp = []
        for data in result[table]:
            value = data['value']['extract_data']
            block_path = data['block_path']
            item_id = data['item_id']
            tmp.append(table(
                value=value,
                ns=clock,
                clock=clock,
                item_id=item_id,
                block_path=block_path
            ))
        table.objects.bulk_create(tmp)


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
                clock=clock,
                item_id=item_id
            ))
        table.objects.bulk_create(tmp)


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
    db_module = importlib.import_module(TRIGGER_DB_MODULES)
    if hasattr(db_module, table_name) is False:
        raise Exception("%s table isn't exist" % table_name)
    table = getattr(db_module, table_name)
    return table

if __name__ == "__main__":
    rules = get_all_rule()
    print rules
