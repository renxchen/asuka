import os
class DevicesConstants(object):
    """
    Define value for devices service
    valid period format e.g:"2017-12-12@12:12;2017-12-12@13:12"
    schedule format e.g:"week1;week2;week3@09:00-10:00"
    Period type
    0:open valid period type
    1:close valid period type
    Schedule type
    0: start collection normally
    1: stop collection at anytime
    2: start collection at specially
    """
    OPEN_VALID_PERIOD_TYPE = 1
    VALID_PERIOD_SPLIT = ";"
    VALID_DATE_FORMAT = "%Y-%m-%d@%H:%M"
    SCHEDULE_GET_NORMALLY = 0
    SCHEDULE_CLOSED = 1
    SCHEDULE_SPECIALLY = 2
    SCHEDULE_WEEKS_SPLIT = ";"
    SCHEDULE_DATE_SPLIT = "@"
    SCHEDULE_SPLIT = "-"
    CLI_COLLECTION_DEFAULT_METHOD = 'telnet'
    SNMP_COLLECTION_DEFAULT_METHOD = "bulk_get"


class CommonConstants(object):
    """
    Define value for common service
    """
    VALUE_TYPE_MAPPING = {
        0: "Int",
        1: "Text",
        2: "Float",
        3: "Str"
    }
    ITEM_TYPE_MAPPING = {
        0: "Cli",
        1: "Snmp"
    }
    SNMP_TYPE_CODE = 1
    CLI_TYPE_CODE = 0
    ALL_TYPE_CODE = -1
    MEM_CACHE_HOSTS = [('10.71.244.134:11211', 1), ]


class TriggerConstants(object):
    """
    Define value for trigger service
    """
    TRIGGER_DB_MODULES = "apolo_server.processor.db_units.models"
    TRIGGER_BASE_PATH = "apolo_server.processor.trigger"
    TRIGGER_NUMERIC = ["Float", "Int"]
    TRIGGER_EVENT_SOURCE = 0
    TRIGGER_OPEN = 0
    TRIGGER_CLOSE = 1
    TRIGGER_VALUE = 1
    NORMAL_VALUE = 0
    FUNCTION_LIST = ["Hex2Dec", "Ave", "Max", "Min", "A", "B"]


class ParserConstants(object):
    """
    Define constant value for parser service
    """
    TREE_PATH_SPLIT = "/"


class ActionConstants(object):
    """
    Action constant value for action service
    """
    SNMP_TARGET_SERVER = "10.79.148.107"
    DEFAULT_ENTERPRISE_OID = "1.3.6.1.4.1.2345"
    BASE_SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "script")
    if os.path.exists(BASE_SCRIPT_PATH) is False:
        os.mkdir(BASE_SCRIPT_PATH)
