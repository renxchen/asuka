"""
############Common###########
"""
VALUE_TYPE_MAPPING = {
    0: "Int"
}
ITEM_TYPE_MAPPING = {
    0: "Cli",
    1: "Snmp"
}


"""
############Collection###########
"""
"""
# valid period format e.g:"2017-12-12@12:12;2017-12-12@13:12"
# schedule format e.g:"week1;week2;week3@09:00-10:00"
"""

"""
# 0:open valid period type
# 1:close valid period type
"""
OPEN_VALID_PERIOD_TYPE = 0

VALID_PERIOD_SPLIT = ";"
VALID_DATE_FORMAT = "%Y-%m-%d@%H:%M"

"""
# 0: start collection normally
# 1: stop collection at anytime
# 2: start collection at specially
"""
SCHEDULE_GET_NORMALLY = 0
SCHEDULE_CLOSED = 1
SCHEDULE_SPECIALLY = 2

SCHEDULE_WEEKS_SPLIT = ";"
SCHEDULE_DATE_SPLIT = "@"
SCHEDULE_SPLIT = "-"

CLI_COLLECTION_DEFAULT_METHOD = 'telnet'
SNMP_COLLECTION_DEFAULT_METHOD = "bulk_get"

"""
############Trigger###########
"""
TRIGGER_DB_MODULES = "Venus.db_units.models"
TRIGGER_NUMERIC = ["Float", "Int"]
TRIGGER_EVENT_SOURCE = 0
TRIGGER_OPEN = 0
TRIGGER_CLOSE = 1
TRIGGER_VALUE = 1
NORMAL_VALUE = 0

"""
##########Parser###########
"""
TREE_PATH_SPLIT = "/"
