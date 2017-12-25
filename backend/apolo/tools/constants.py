#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright 2017 Cisco Systems, Inc.
# All rights reserved.
#########################################
# PATHS
#########################################
LOG_PATH = 'apolo/logs/logger_authentication.log'
#########################################
# API response status define
#########################################
STATUS = 'status'
REFRESH_CODE = 101
NO_REFRESH_CODE = 100
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
TOKEN = 'token'
SUPERUSER = 'superuser'
ADMIN = 'admin'
STAFF = 'staff'
ROLE = 'role'
ORIG_IAT = 'orig_iat'
NEW_TOKEN = "NEW_TOKEN"
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
BLOCK_RULE_TREE_KIND_ONE_NAME ='b1'    # インデントによって絞る
BLOCK_RULE_TREE_KIND_TWO_NAME = 'b2'   #  行数によって絞る
BLOCK_RULE_TREE_KIND_THREE_NAME ='b3'  #  指定文字列の間
DATA_RULE_TREE_KIND_ONE_NAME = 'd1'    #  特定文字からの距離
DATA_RULE_TREE_KIND_TWO_NAME = 'd2'    #  行数指定
DATA_RULE_TREE_KIND_THREE_NAME ='d3'   #  正規表現
POLICY_TREE_ROOT_ICON = 'pcy_root_icon.jpg'
BLOCK_NODE_ICON = 'rule_block_node_icon.jpg'
DATA_NODE_ICON = 'rule_data_node_icon.jpg'
RULE_NODE_ICON = 'rule_tree_node_icon.jpg'


