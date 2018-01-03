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
BLOCK_RULE_TREE_KIND_ONE_NAME = 'b1'  # インデントによって絞る
BLOCK_RULE_TREE_KIND_TWO_NAME = 'b2'  # 行数によって絞る
BLOCK_RULE_TREE_KIND_THREE_NAME = 'b3'  # 指定文字列の間
BLOCK_RULE_TREE_KIND_FOUR_NAME = 'b4'  # 正規表現による絞る
DATA_RULE_TREE_KIND_ONE_NAME = 'd1'  # 特定文字からの距離
DATA_RULE_TREE_KIND_TWO_NAME = 'd2'  # 行数指定
DATA_RULE_TREE_KIND_THREE_NAME = 'd3'  # 正規表現
DATA_RULE_TREE_KIND_FOUR_NAME = 'd4'  # データ行数を取得
POLICY_TREE_ROOT_ICON = 'pcy_root_icon.jpg'
BLOCK_NODE_ICON = 'rule_block_node_icon.jpg'
DATA_NODE_ICON = 'rule_data_node_icon.jpg'
RULE_NODE_ICON = 'rule_tree_node_icon.jpg'

#########################################
# Policy Tree Message
#########################################
NODE_IS_EXISTENCE = 'the node exist in the tree'  # ツリー内に定義されているため、編集できません。
RULE_NAME_IS_EXISTENCE = 'the same name rule is existence'  # 既に同じ表示名のルールが登録されています。
POLICY_IS_APPLIED = 'the policy is being applied by schedule function'  # このコレクションポリシーがスケジュールに利用されています。
POLICY_DATA_VALID_ERROR = 'data valid error when insert policy tree rules'  # コレクションポリシーツリーに追加されたデータが適切ではないです。
RULE_DATA_VALID_ERROR = 'data valid error in saving the rule'  # ルールを追加する時に、データが適切ではないです
LOAD_RULE_TYPE_ERROR = 'rule type is not defined'  # ルールのタイプが定義されていないです
