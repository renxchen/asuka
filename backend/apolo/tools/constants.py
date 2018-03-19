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
SUCCESS = 'Success'
FAILED = 'Failed'
TRUE = 'True'
FALSE = 'False'
VERIFY_WHETHER_EXECUTING_SERVER_URL = "http://%s:%s/api/v1/valid"
VERIFY_WHETHER_EXECUTING_SERVER_IP = '10.71.244.134'
VERIFY_WHETHER_EXECUTING_SERVER_PORT = '7777'
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
TOKEN_NOT_EXIST_FOR_CURRENT_USER_MSG = 'There was no token found for current user.'
NO_USERNAME_OR_PASSWORD_FONUD_ERROR = "No username or password found, username is %s, password is %s."
LOGIN_FAILED_ERROR = "Login failed with incorrect username %s or password %s."
REFRESH_EXPIRED = "Refresh has expired."
ORIG_IAT_REQUIRED = "orig_iat field is required."
USERNAME_INACTIVE_ERROR = "Username %s is inactive."
LOGIN_SUCCESSFUL = "Login successful with username %s and password %s."
NO_USERNAME_OR_PASSWORD = "No user or password found."
USER_AND_PASSWD_INCORRECT = "User or password is incorrect."
USER_DISABLED = "User is disabled."
USER_LOGOUT_SUCCESSFUL = "User logout successful."
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
COLUMN_A_OR_COLUMN_B_NOT_EXIST = 'Column A(column_a as table id %s) or Column B(column_b as table id %s) is not exist in current system, please connect Administrator.'
COLUMN_A_COLUMN_B_VERIFY_FAILED = 'Column A and Column B maybe do not belong to the same device group or value type(String or Integer) or policy type(CLI or SNMP).'
EXPRESSION_ILLEGAL = gettext('There is illegal format in current expression, legal formats like: A[1], B[1], A(1), B(1)')
EXPRESSION_A_B_VALUE_TYPE_NOT_SAME = 'A and B maybe do not have the same value type(String or Integer)'
EXPRESSION_A_B_NOT_EXIST = 'There is not A or B in expression, should be at least A in expression'
EXPRESSION_CONDITION_ILLEGAL = 'The expression condition should be in <=, >=, ==, !=, >, <'
EXPRESSION_ILLEGAL_IN_LEFT_EXPRESSION = 'There is illegal format in current expression, illegal character %s exist in left expression'
EXPRESSION_ILLEGAL_IN_RIGHT_EXPRESSION = 'There is illegal format in current expression, illegal character %s exist in right expression'
EXPRESSION_EVAL_VERIFY_FAILED = 'The expression %s eval verification failed.'
EXPRESSION_VERIFY_FAILED = 'The expression verify failed'
ACTION_POLICY_NAME_DUPLICATE = 'The action name is exist in current system, please change name.'
DATA_TABLE_NAME_DUPLICATE = 'The table name is exist in current system, please change name.'
OSTYPE_EXIST_IN_SCHEDULE = 'OSTYPE_EXIST_IN_SCHEDULE'
DEVICE_GROUP_NOT_EXIST = 'Current device group is not exist in current system.'
DEVICE_GROUP_NOT_EXIST_IN_SCHEDULE = gettext('Current device group is not exist in Schedule Table.')
DATA_TABLE_NOT_EXIST_IN_SYSTEM = gettext('Current data table is not exist in system.')
#########################################
# Collection Policy Related define
#########################################
# data extra related
SPLIT_RULE_SPACE = 'space'
SPLIT_RULE_COMMA = 'comma'
SPLIT_RULE_SLASH = 'slash'
SPLIT_RULE_OTHER = 'other'
INSTEAD = '@@'
NO_MATCH_EXTRACT_DATA_REGEXP = 'Can not match the provided regular Expression.'

# collection policy functional related
COLLECTION_POLICY_NOT_EXIST = 'The collection policy is not exist with id %s.'
COLLECTION_POLICY_IS_EXECUTING = 'The Collection policy is running in system with id %s.'
COLL_POLICY_EXIST_IN_ITEM = 'COLL_POLICY_EXIST_IN_ITEM'
COLL_POLICY_EXIST_IN_POLICYS_GROUPS = 'COLL_POLICY_EXIST_IN_POLICYS_GROUPS'
COLLECTION_POLICY_NAME_DUPLICATE = 'CP_NAME_DUPLICATE'
#########################################
# Collection Policy Group Related define
#########################################
COLL_POLICY_GROUP_EXIST_IN_SCHEDULE = 'COLL_POLICY_GROUP_EXIST_IN_SCHEDULE'
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
NODE_IS_EXISTENCE = 'the node exist in the tree'  # ツリー内に定義されているため、編集できません。
RULE_NAME_IS_EXISTENCE = 'RULE_NAME_IS_EXISTENCE'  # 既に同じ表示名のルールが登録されています。
POLICY_IS_APPLIED = 'the policy is being applied by schedule function'  # このコレクションポリシーがスケジュールに利用されています。
POLICY_DATA_VALID_ERROR = 'data valid error when insert policy tree rules'  # コレクションポリシーツリーに追加されたデータが適切ではないです。
RULE_DATA_VALID_ERROR = 'data valid error in saving the rule'  # ルールを追加する時に、データが適切ではないです
LOAD_RULE_TYPE_ERROR = 'rule type is not defined'  # ルールのタイプが定義されていないです
DB_EXCEPTION = 'there is an db exception'
RULE_ID_IS_USED = 'RULE_ID_USED'  # ルールが利用されています
CP_NAME_DUPLICATE = 'CP_NAME_DUPLICATE'
#########################################
# value_type of policy tree rule
#########################################
VALUE_TYPE_INT = 1
VALUE_TYPE_FLOAT = 2
VALUE_TYPE_STRING = 3
VALUE_TYPE_TEXT = 4
#########################################
# data collection value setting
#########################################
SCHEDULE_STATUS_DEFAULT = 1
ITEM_TABLE_STATUS_DEFAULT = 0
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
# 各グループにおけるあるデバイスとあるコレクションポリシーが紐付いています。かつ、同じ優先度が同じです。追加不可です。
POLICY_DEVICE_COMBINATION = 'the combination of policy and device is used' # device id and policy id の組み合わせが利用されている
CAN_NOT_DELETE_SCHEDULE_MESSAGE = 'can not delete schedule data'
CAN_NOT_UPDATE_SCHEDULE_MESSAGE = 'can not update schedule data'
NO_ITEMS_IN_GROUP = 'no items in group,please check the group'
DATA_COLLECTION_POST_URL = 'http://10.71.244.134:7777/api/v1/getItems'
POLICY_POST_URL = 'http://10.71.244.134:7777/api/v1/valid'
#########################################
# render
#########################################
X_OFFSET_ERROR = 'XOffset is too long'
Y_OFFSET_ERROR = 'YOffset is too long'
NOT_MATCH_BASIC_CHAR = 'can not find the basic char'
NO_EXTRACT_LINE_NUM = 'no lines'
NO_EXTRACT_DATA = 'no extract data'
LEAF_IS_BLOCK_RULE = 'LEAF_IS_BLOCK_RULE'
POLICY_TREE_IS_GROUPED = 'policy tree is grouped'
#################################################################
# instead mark string
REPLACE_START_MARK = '☆start☆'
REPLACE_END_MARK = '☆end☆'
LINE_NUM_MSG_REPLACE = '◇◎◎◇' #'@##@'
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
# Other API information define
#########################################
