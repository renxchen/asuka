#!/usr/bin/env python
# coding=utf-8
"""

@author: kimli
@contact: kimli@cisco.com
@file: data_table_name_verify.py
@time: 2018/1/21 20:25
@desc:

"""
import traceback
from rest_framework import viewsets
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return
from backend.apolo.tools import constants
from backend.apolo.tools import views_helper
from backend.apolo.models import DataTable


class DataTableNameVerifyViewsSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(DataTableNameVerifyViewsSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        method = 'GET'
        if request.method.lower() == 'get':
            method = 'GET'
        if request.method.lower() == 'post' or request.method.lower() == 'put':
            method = 'BODY'
        self.name = views_helper.get_request_value(self.request, 'name', method)

    @staticmethod
    def get_data_table(**kwargs):
        """!@brief
        Get the data of DataTable table
        @param kwargs: dictionary type of the query condition
        @pre call when need data of DataTable table
        @post return DataTable data
        @return result: data of DataTable table
        """
        try:
            dt = DataTable.objects.filter(**kwargs)
            return dt
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def get(self):
        """!@brief
        Rest Api of GET, verify whether data table name was exist
        @return data: the status
        """
        try:
            if self.name is not '':
                get_name_from_data_table = self.get_data_table(**{'name': self.name})
                data = {
                    constants.STATUS: {
                        constants.STATUS: constants.TRUE,
                        constants.MESSAGE: constants.SUCCESS
                    }
                }
                if len(get_name_from_data_table) > 0:
                    data = {
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.DATA_TABLE_NAME_DUPLICATE
                        }
                    }
                return api_return(data=data)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)
