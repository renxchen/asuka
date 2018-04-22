import os

SYS_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


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
    TASK_START_TIME = {
        900: [10],
        3600: [0],
        86400: [1, 0]
    }


class CommonConstants(object):
    """
    Define value for common service
    """
    VALUE_TYPE_MAPPING = {
        0: "int",
        1: "text",
        2: "float",
        3: "str"
    }
    ITEM_TYPE_MAPPING = {
        0: "Cli",
        1: "Snmp"
    }
    SNMP_TYPE_CODE = 1
    CLI_TYPE_CODE = 0
    ALL_TYPE_CODE = -1
    MEM_CACHE_HOSTS = [('10.71.244.134:11211', 1), ]
    ALL_FINISH_CHECK_FLAG="ALL_FINISH"


class TriggerConstants(object):
    """
    Define value for trigger service
    """
    TRIGGER_DB_MODULES = "backend.apolo.models"
    TRIGGER_BASE_PATH = "apolo_server.processor.trigger"
    TRIGGER_NUMERIC = ["Float", "Int"]
    TRIGGER_EVENT_SOURCE = 0
    TRIGGER_OPEN = 0
    TRIGGER_CLOSE = 1
    TRIGGER_VALUE = 1
    NORMAL_VALUE = 0
    TRIGGERD = 1
    NOT_TRIGERD=0
    FUNCTION_LIST = ["Hex2Dec", "Ave", "Max", "Min", "A", "B"]
    PRIORITY_STANDARD_LEVEL_VALUE = 0
    PRIORITY_HIGH_LEVEL_VALUE = 1
    PRIORITY_URGENT_LEVEL_VALUE = 2

    TRIGGER_TYPE_EXPRESSION_COMPARE = 0
    TRIGGER_TYPE_INTEGER_COMPARE = 1
    TRIGGER_TYPE_STRING__COMPARE = 2
    TRIGGER_TYPE_FAILED = 3

    TAKE_ACTION=1
    NO_ACTION=0

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
    ACTION_TYPE_MAPPING = {
        0: "SnmpTrapAction",
        1: "ScriptAction",
        2: "RundeckAction"
    }
    ACTION_TYPE_MAPPING2 = {
        0: "SnmpTrap",
        1: "Script",
        2: "Rundeck"
    }
