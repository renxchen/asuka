#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright 2017 Cisco Systems, Inc.
# All rights reserved.
#########################################
# PATHS
#########################################
LOG_PATH = 'logs/logger_authentication.log'

#########################################
# API token related define
#########################################
REFRESH_CODE = 101
NO_REFRESH_CODE = 100
TOKEN_ALREADY_EXPIRED_CODE = 102
TOKEN_NOT_EXIST_FOR_CURRENT_USER_CODE = 103
TOKEN = 'token'
NEW_TOKEN = "NEW_TOKEN"
TOKEN_EXPIRED_MSG = 'Signature has expired.'
TOKEN_NOT_EXIST_FOR_CURRENT_USER_MSG = 'There was no token found for current user.'
#########################################
# API response status define
#########################################
STATUS = 'status'
CODE = 'code'
SUCCESS = 'Success'
FAILED = 'Failed'
TRUE = 'True'
FALSE = 'False'
#########################################
# API parameters define
#########################################
USERNAME = 'username'
PASSWORD = 'password'
MESSAGE = 'message'
SUPERUSER = 'superuser'
ADMIN = 'admin'
STAFF = 'staff'
ROLE = 'role'
ORIG_IAT = 'orig_iat'
TIMEDELTA = 120
#########################################
# API information define
#########################################
NO_USERNAME_OR_PASSWORD = "No user or password found."
USER_AND_PASSWD_INCORRECT = "User or password is incorrect."
USER_DISABLED = "User is disabled."
USER_LOGOUT_SUCCESSFUL = "User logout successful."
COLLECTION_POLICY_NAME_DUPLICATE = 'CP_NAME_DUPLICATE'
#########################################
# API log or exception define
#########################################
REFRESH_EXPIRED = "Refresh has expired."
ORIG_IAT_REQUIRED = "orig_iat field is required."
KEY_ERROR = "Mapping key of %s not found."
PAGE_NOT_INTEGER = "That page number is not an integer."
EMPTY_PAGE = "That page number is less than 1."
NO_USERNAME_OR_PASSWORD_FONUD_ERROR = "No username or password found, username is %s, password is %s."
LOGIN_FAILED_ERROR = "Login failed with incorrect username %s or password %s."
USERNAME_INACTIVE_ERROR = "Username %s is inactive."
LOGIN_SUCCESSFUL = "Login successful with username %s and password %s."
#########################################
# API Collection policy
#########################################
SPLIT_RULE_SPACE = 'space'
SPLIT_RULE_COMMA = 'comma'
SPLIT_RULE_SLASH = 'slash'
SPLIT_RULE_OTHER = 'other'
INSTEAD = '@@'
NO_MATCH_EXTRACT_DATA_REGEXP = 'Can not match the provided regular Expression.'

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
DATA_RULE_TREE_KIND_THREE_NAME ='正規表現'
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
RULE_NAME_IS_EXISTENCE = 'the same name rule is existence'  # 既に同じ表示名のルールが登録されています。
POLICY_IS_APPLIED = 'the policy is being applied by schedule function'  # このコレクションポリシーがスケジュールに利用されています。
POLICY_DATA_VALID_ERROR = 'data valid error when insert policy tree rules'  # コレクションポリシーツリーに追加されたデータが適切ではないです。
RULE_DATA_VALID_ERROR = 'data valid error in saving the rule'  # ルールを追加する時に、データが適切ではないです
LOAD_RULE_TYPE_ERROR = 'rule type is not defined'  # ルールのタイプが定義されていないです
DB_EXCEPTION ='there is an db exception'

#########################################
# data collection value setting
#########################################
SCHEDULE_STATUS_DEFAULT = 0
ITEM_TABLE_STATUS_DEFAULT = 0
ITEM_TYPE_CLE = 0
ITEM_TYPE_SNMP = 1
VALUE_TYPE = {
    'INT': 0,
    'FLOAT': 1,
    'STRING': 2
}
LEAF_NODE_MARK = 1
#########################################
# data collection Error Message
#########################################
# 各グループにおけるあるデバイスとあるコレクションポリシーが紐付いています。かつ、同じ優先度が同じです。追加不可です。
POLICY_DEVICE_COMBINATION = 'the combination of policy and device  is used'
CAN_NOT_DELETE_SCHEDULE_MESSAGE = 'can not delete schedule data'
CAN_NOT_UPDATE_SCHEDULE_MESSAGE = 'can not update schedule data'

