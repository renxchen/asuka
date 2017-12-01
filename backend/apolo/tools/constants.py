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
SUCCESS = 'SUCCESS'
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
NO_USERNAME_OR_PASSWORD = "NO_USERNAME_OR_PASSWORD"
USER_AND_PASSWD_INCORRECT = "USER_AND_PASSWD_INCORRECT"
USER_DISABLED = "USER_DISABLED"
USER_LOGOUT_SUCCESSFUL = "USER_LOGOUT_SUCCESSFUL"
#########################################
# API log or exception define
#########################################
REFRESH_EXPIRED = "Refresh has expired."
ORIG_IAT_REQUIRED = "orig_iat field is required."
KEY_ERROR = "Mapping key of %s not found."
NO_USERNAME_OR_PASSWORD_FONUD_ERROR = "No username or password found, username is %s, password is %s."
LOGIN_FAILED_ERROR = "Login failed with incorrect username %s or password %s."
USERNAME_INACTIVE_ERROR = "Username %s is inactive."
LOGIN_SUCCESSFUL = "Login successful with username %s and password %s."
