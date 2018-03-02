#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

@author: kimli
@contact: kimli@cisco.com
@file: action_policy_column_views.py
@time: 2018/2/12 12:34
@desc:

"""
import traceback
import importlib
from rest_framework import viewsets
from django.utils.translation import gettext
from django.core.paginator import Paginator
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return
from backend.apolo.tools import constants
from backend.apolo.tools import views_helper
from backend.apolo.models import Triggers, TriggerDetail, DataTableItems
from django.db import transaction
from backend.apolo.serializer.action_policy_serializer import TriggerSerializer, ActionsSerializer, \
    TriggerDetailSerializer
import time
import simplejson as json
import logging


class ActionPolicyColumnViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(ActionPolicyColumnViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        self.page_from = views_helper.get_request_value(self.request, 'page', 'GET')
        self.max_size_per_page = views_helper.get_request_value(self.request, 'rows', 'GET')
        self.logger = logging.getLogger("apolo.error")
        method = 'GET'
        if request.method.lower() == 'get' or request.method.lower() == 'delete':
            method = 'GET'
        if request.method.lower() == 'post' or request.method.lower() == 'put':
            method = 'BODY'
        self.table_id = views_helper.get_request_value(self.request, 'id', method)

    def get(self):
        try:
            pass
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def post(self):
        try:
            with transaction.atomic():
                pass
        except Exception, e:
            transaction.rollback()
            if True:
                print traceback.format_exc(e)
            self.logger.error(e)
            return exception_handler(e)

    def put(self):
        try:
            with transaction.atomic():
                pass
        except Exception, e:
            transaction.rollback()
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def delete(self):
        try:
            with transaction.atomic():
                pass
        except Exception, e:
            transaction.rollback()
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)
