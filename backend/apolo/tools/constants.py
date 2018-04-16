#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright 2017 Cisco Systems, Inc.
# All rights reserved.

from django.utils.translation import gettext

#########################################
# Logs and CSV export paths
#########################################
LOG_PATH = 'logs/system_logger.log'
CSV_PATH = 'export/apolo_export.csv'
#########################################
# API Debug Flag, True: if true, the system will print detail debug information
#########################################
DEBUG_FLAG = True
#########################################
# API Common constant define
#########################################
NUMBER_ZERO = 0
NUMBER_ONE = 1
NUMBER_TWO = 2
NUMBER_THREE = 3
NUMBER_FOUR = 4
NUMBER_FIVE = 5
NUMBER_SIX = 6
NUMBER_SEVEN = 7
NUMBER_EIGHT = 8
NUMBER_NINE = 9
MESSAGE = 'message'
STATUS = 'status'
CODE = 'code'
MSG_TYPE = 'type'
SUCCESS = 'Success'
FAILED = 'Failed'
TRUE = 'True'
FALSE = 'False'
VERIFY_WHETHER_EXECUTING_SERVER_URL = "http://%s:%s/api/v1/valid"
VERIFY_WHETHER_EXECUTING_SERVER_IP = '127.0.0.1'
VERIFY_WHETHER_EXECUTING_SERVER_PORT = '7777'
VERIFY_WHETHER_CAN_CONNECT_URL = "http://%s:%s/api/v1/devicestatus"
SYSTEM_ERROR = gettext('System access failed, please connect the administrator.')
POST_SUCCESSFUL = gettext('Data create successfully.')
PUT_SUCCESSFUL = gettext('Data update successfully.')
DELETE_SUCCESSFUL = gettext('Data delete successfully.')
#########################################
# API token related define
#########################################
REFRESH_CODE = 101
NO_REFRESH_CODE = 100
TOKEN_ALREADY_EXPIRED_CODE = 102
TOKEN_NOT_EXIST_FOR_CURRENT_USER_CODE = 103
TOKEN_TIMEDELTA = 120
TOKEN = 'token'
NEW_TOKEN = "NEW_TOKEN"
SUPERUSER = 'superuser'
ADMIN = 'admin'
STAFF = 'staff'
ROLE = 'role'
ORIG_IAT = 'orig_iat'
USERNAME = 'username'
PASSWORD = 'password'
TOKEN_EXPIRED_MSG = gettext('Token has expired.')
TOKEN_NOT_EXIST_FOR_CURRENT_USER_MSG = gettext('There was no token found for current user.')
NO_USERNAME_OR_PASSWORD_FONUD_ERROR = gettext("No access, please login first.")
LOGIN_FAILED_ERROR = gettext("Login failed with incorrect username or password.")
REFRESH_EXPIRED = gettext("Access is expired, please login again.")
ORIG_IAT_REQUIRED = gettext("orig_iat field is required.")
USERNAME_INACTIVE_ERROR = gettext("Username is inactive.")
LOGIN_SUCCESSFUL = gettext("Login successful.")
NO_USERNAME_OR_PASSWORD = gettext("No user or password found.")
USER_AND_PASSWD_INCORRECT = gettext("User or password is incorrect.")
USER_DISABLED = gettext("User is inactive.")
USER_LOGOUT_SUCCESSFUL = gettext("User logout successful.")
#########################################
# Action Policy Related define
#########################################
EQUAL_SIGN = '='
GREATER_THAN_SIGN = '>'
LESS_THAN_SIGN = '<'
GREATER_THAN_OR_EQUAL_SIGN = '>='
LESS_THAN_OR_EQUAL_SIGN = '<='
NOT_EQUAL_SIGN = '!='
PRIORITY_CRITICAL = 'CRITICAL'
PRIORITY_MAJOR = 'MAJOR'
PRIORITY_MINOR = 'MINOR'
SNMP = 'snmp'
CLI = 'cli'
FLOAT = 'float'
STRING = 'string'
TEXT = 'text'
INTEGER = 'int'
TRIGGER_TYPE_EXPRESSION_COMPARE = '演算比較'
TRIGGER_TYPE_INTEGER_COMPARE = '数値比較'
TRIGGER_TYPE_STRING__COMPARE = '文字列比較'
TRIGGER_TYPE_FAILED = '取得失敗'
COLUMN_A_OR_COLUMN_B_NOT_EXIST = gettext(
    'Column A or Column B is not exist in current system, please connect Administrator.')
COLUMN_A_COLUMN_B_VERIFY_FAILED = gettext(
    'Column A and Column B may do not have the same device group or schedule or collectionNo access, please login first. interval.')
EXPRESSION_ILLEGAL = gettext(
    'There is illegal format in current expression, legal formats like: A[1], B[1], A(1), B(1).')
EXPRESSION_A_B_VALUE_TYPE_NOT_SAME = gettext('A and B maybe do not have the same value type(String or Integer).')
EXPRESSION_A_B_NOT_EXIST = gettext('There is not A or B in expression, should be at least A in expression.')
EXPRESSION_CONDITION_ILLEGAL = gettext('The expression condition should be in <=, >=, ==, !=, >, <.')
EXPRESSION_ILLEGAL_IN_LEFT_EXPRESSION = gettext('There is illegal format in current expression.')
EXPRESSION_EVAL_VERIFY_FAILED = gettext('The expression eval verification failed.')
EXPRESSION_VERIFY_FAILED = gettext('The expression verify failed')
ACTION_POLICY_NAME_DUPLICATE = gettext('The action name is exist in current system, please change name.')
DATA_TABLE_NAME_DUPLICATE = gettext('The table name is exist in current system, please change name.')
OSTYPE_EXIST_IN_SCHEDULE = gettext('Ostype is in use.')
DEVICE_GROUP_NOT_EXIST = gettext('Current device group is not exist in current system.')
DEVICE_GROUP_NOT_EXIST_IN_SCHEDULE = gettext('Current device group is not exist in Schedule Table.')
DATA_TABLE_NOT_EXIST_IN_SYSTEM = gettext('Current data table is not exist in system.')
DATA_TABLE_EXIST_IN_TRIGGER = gettext('Current data table is running in action policy.')
CSV_PATH_NOT_EXIST = gettext('CSV path is not exist.')
DATA_TABLE_PROORITY_0 = '高'
DATA_TABLE_PROORITY_1 = '标准'
#########################################
# Collection Policy Related define
#########################################
# data extra related
SPLIT_RULE_SPACE = 'space'
SPLIT_RULE_COMMA = 'comma'
SPLIT_RULE_SLASH = 'slash'
SPLIT_RULE_OTHER = 'other'
INSTEAD = '@@'  # '△△'
NO_MATCH_EXTRACT_DATA_REGEXP = gettext('Can not match the provided regular Expression.')

# collection policy functional related
COLLECTION_POLICY_NOT_EXIST = gettext('The collection policy is not exist in system.')
COLLECTION_POLICY_IS_EXECUTING = gettext('The collection policy is running in system.')
COLL_POLICY_EXIST_IN_ITEM = 'COLL_POLICY_EXIST_IN_ITEM'
COLL_POLICY_EXIST_IN_POLICYS_GROUPS = gettext('Collection policy group is exist in system.')
COLLECTION_POLICY_NAME_DUPLICATE = gettext('Collection policy name is exist in system.')
#########################################
# Collection Policy Group Related define
#########################################
COLL_POLICY_GROUP_NOT_FOUND = gettext('Collection policy group not exist in system.')
COLLECTION_POLICY_GROUP_NAME_DUPLICATE = gettext('Collection policy group name is exist in system.')
COLL_POLICY_GROUP_EXIST_IN_SCHEDULE = gettext('Collection policy group is running in system.')
#########################################
# Policy Tree Node's information
# Rule Tree Node's information
#########################################
COLLECTION_POLICY_TREE_NAME = 'ルールツリー定義'
BLOCK_RULE_TREE_KIND_ONE_NAME = 'インデントによって絞る'
BLOCK_RULE_TREE_KIND_TWO_NAME = '行数によって絞る'
BLOCK_RULE_TREE_KIND_THREE_NAME = '指定文字列の間'
BLOCK_RULE_TREE_KIND_FOUR_NAME = '正規表現による絞る'
DATA_RULE_TREE_KIND_ONE_NAME = '特定文字からの距離'
DATA_RULE_TREE_KIND_TWO_NAME = '行数指定'
DATA_RULE_TREE_KIND_THREE_NAME = '正規表現'
DATA_RULE_TREE_KIND_FOUR_NAME = 'データ行数を取得'
DATA_RULE_TREE_KIND_FIVE_NAME = '出力全抽出機能'
POLICY_TREE_ROOT_ICON = 'fa fa-tags fa-lg'
BLOCK_NODE_ICON = 'fa fa-cubes'
DATA_NODE_ICON = 'fa fa-text-height'
RULE_NODE_ICON = 'fa fa-folder-o'
#########################################
# Policy Tree Message
#########################################
NODE_IS_EXISTENCE = gettext('The node is exist in the tree')  # ツリー内に定義されているため、編集できません。
RULE_NAME_IS_EXISTENCE = 'RULE_NAME_IS_EXISTENCE'  # 既に同じ表示名のルールが登録されています。
POLICY_IS_APPLIED = gettext('The policy is be setting in schedule function.')  # このコレクションポリシーがスケジュールに利用されています。
POLICY_DATA_VALID_ERROR = gettext('Data valid error when insert policy tree rules')  # コレクションポリシーツリーに追加されたデータが適切ではないです。
RULE_DATA_VALID_ERROR = gettext('Data valid error in saving the rule')  # ルールを追加する時に、データが適切ではないです
LOAD_RULE_TYPE_ERROR = gettext('Rule type is not defined')  # ルールのタイプが定義されていないです
DB_EXCEPTION = gettext('There is an db exception')
RULE_ID_IS_USED = 'RULE_ID_USED'  # ルールが利用されています
CP_NAME_DUPLICATE = 'CP_NAME_DUPLICATE'
#########################################
# value_type of policy tree rule
#########################################
VALUE_TYPE_INT = 0
VALUE_TYPE_FLOAT = 2
VALUE_TYPE_STRING = 3
VALUE_TYPE_TEXT = 1
#########################################
# data collection value setting
#########################################
SCHEDULE_STATUS_DEFAULT = 1
ITEM_TABLE_STATUS_DEFAULT = 1
ITEM_TYPE_CLI = 0  # cli
ITEM_TYPE_SNMP = 1  # snmp
VALUE_TYPE = {
    'INT': 0,
    'FLOAT': 1,
    'STRING': 2
}
LEAF_NODE_MARK = 1
########################################
# Mapping data
########################################
PRIORITY_STANDARD_LEVEL_VALUE = 0
PRIORITY_STANDARD_LEVEL_KEY = u'標準'
PRIORITY_HIGH_LEVEL_VALUE = 1
PRIORITY_HIGH_LEVEL_KEY = u'高'
PRIORITY_URGENT_LEVEL_VALUE = 2
PRIORITY_URGENT_LEVEL_KEY = u'緊急'

SCHEDULE_TYPE_OFTEN_KEY = u'常に取得'
SCHEDULE_TYPE_OFTEN_VALUE = 0
SCHEDULE_TYPE_STOP_KEY = u'取得停止'
SCHEDULE_TYPE_STOP_VALUE = 1
SCHEDULE_TYPE_PERIOD_KEY = u'周期取得'
SCHEDULE_TYPE_PERIOD_VALUE = 2

SCHEDULE_STATUS_ON_KEY = u'有効'
SCHEDULE_STATUS_ON_VALUE = 1
SCHEDULE_STATUS_OFF_KEY = u'無効'
SCHEDULE_STATUS_OFF_VALUE = 0

CP_STATUS_OFF_KEY = u'停止'
CP_STATUS_OFF_VALUE = 0
CP_STATUS_ON_KEY = u'取得中'
CP_STATUS_ON_VAULE = 1

#########################################
# data collection Error Message
#########################################

POLICY_DEVICE_COMBINATION = gettext('There is the same configure in the schedule')  # 同一のコレクションポリシー、ディバイスと優先度が設定されています
CAN_NOT_DELETE_SCHEDULE_MESSAGE = gettext('Can not delete schedule data')
CAN_NOT_UPDATE_SCHEDULE_MESSAGE = gettext('Can not update schedule data')
NO_DEVICE_IN_DEVICE_GROUP = gettext('There is no device in device group,please check the group')
NO_CP_IN_CP_GROUP = gettext('There is no policy in policy group,please check the group')
NULL_TREE_IN_CP = gettext('There is a null tree in the collection policy')
#########################################
# render
#########################################
X_OFFSET_ERROR = gettext('XOffset is too long')
Y_OFFSET_ERROR = gettext('YOffset is too long')
NOT_MATCH_BASIC_CHAR = gettext('Can not find the basic char ')
NO_EXTRACT_LINE_NUM = gettext('No lines')
NO_EXTRACT_DATA = gettext('There are no extract data')
LEAF_IS_BLOCK_RULE = gettext('Because leaf node is block rule,the policy can not be saved!')
POLICY_TREE_IS_GROUPED = gettext('The policy has been set to a policy group')
#################################################################
# instead mark string
REPLACE_START_MARK = '★★'  # '☆start☆'
REPLACE_END_MARK = '☆☆'  # '☆end☆'
LINE_NUM_MSG_REPLACE = '◇◎◎◇'  # '@##@'
# css style of data rule
BASIC_CHAR_STYLE = '<span style="color:#6066c9;text-shadow: 0 0 1px #9c9ff9;">'
EXTRACT_DATA_STYLE = '<span style="color:#0f9f6f;text-decoration: underline;">'
# all line numbers style
EXTRACT_LINE_NUM_STYLE = u'<font color="blue">全 <font color="green"><u>{}</u></font> 行:</font>'
# css style of block rule
BLOCK_BASIC_CHAR_STYLE = '<span style="color:#cf6360;text-shadow: 0 0 1px #cf90cf;">'
BLOCK_RULE_ODD_STYLE = '<div style="background-color:rgba(245, 180, 145, 0.15);display: inline-block;">'
BLOCK_RULE_EVEN_STYLE = '<div style="background-color:rgba(250, 155, 190, 0.15);display: inline-block;">'
REGEXP_BLOCK_RULE_STYLE = '<div style="background-color:rgba(220, 200, 100, 0.2);display: inline-block;">{}</div>'
# end mark
DIV_END = '</div>'
SPAN_END = '</span>'
#########################################
# device, group and ostype information define
#########################################
CSV_TITLE_ERROR = gettext('想定されないフォーマットのCSVが選択されています。登録できません。')
CSV_FORMAT_ERROR = gettext('The type of file is wrong, please check')
CSV_HOSTNAME_EMPTY = gettext('The hostname in csv is empty')
CSV_HOSTNAME_DUPLICATE = gettext('The hostname in csv is repeated')
GROUP_NOT_EXIST = gettext('There is no result for current query.')
GROUP_NAME_FORMAT_ERROR = gettext('The format of group name is incorrect')
EXISTS_IN_DEVICESGROUPS = gettext('このデバイスグループに属しているデバイスが存在するため削除できません。')
EXISTS_IN_SCHEDULES = gettext('The group is already in schedules')
GROUP_ALREADY_EXISTS = gettext('GROUPNAME_ALREADY_EXISTS')
END_DEFAULT_COMMANDS_ERROR = gettext("END_DEFAULT_COMMANDS_ERROR")
START_DEFAULT_COMMANDS_ERROR = gettext("START_DEFAULT_COMMANDS_ERROR")
LOG_FAIL_JUDGES_ERROR = gettext("LOG_FAIL_JUDGES_ERROR")
TELNET_PROMPT_EMPTY_ERROR = gettext("TELNET_PROMPT_EMPTY_ERROR")
TELNET_PROMPT_FORMAT_ERROR = gettext("TELNET_PROMPT_FORMAT_ERROR")
TELNET_TIMEOUT_FORMAT_ERROR = gettext("TELNET_TIMEOUT_FORMAT_ERROR")
SNMP_TIMEOUT_FORMAT_ERROR = gettext("SNMP_TIMEOUT_FORMAT_ERROR")
OSTYPE_NAME_EXISTS = gettext("NAME_IS_EXISTENCE")
OSTYPE_NAME_EMPTY = gettext("Ostype name can not be empty")
OSTYPE_EXIST_IN_DEVICES = gettext("There is device(s) in current ostype!")
OSTYPE_EXIST_IN_SCHEDULE2 = gettext("There is schedule(s) in current ostype!")
OSTYPE_EXISTS_IN_COLL_POLICY = gettext("There is collection policy in current ostype!")
OSTYPE_EXIST_IN_DEVICEGROUPS = gettext("There is device group(s) in current ostype!")
OSTYPE_EXIST_IN_COLL_POLICY_GROUPS = gettext("There is collection policy group(s) in current ostype!")
DEVICE_NOT_EXIST = gettext("There is no device(s) to log in")
#########################################
# Other API information define
#########################################
