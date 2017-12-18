#!/usr/bin/env python
"""

@author: kimli
@contact: kimli@cisco.com
@file: os_type_views.py
@time: 2017/12/18 18:35
@desc:

"""
from backend.apolo.serializer.collection_policy_serializer import OstypeSerializer
from backend.apolo.models import Ostype
from backend.apolo.tools import constants
from rest_framework import viewsets
from backend.apolo.tools.common import api_return
from backend.apolo.tools import views_helper
import traceback
from backend.apolo.tools.exception import exception_handler
import simplejson as json


class OsTypeViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(OsTypeViewSet, self).__init__(**kwargs)
        self.request = request
        self.id = views_helper.get_request_value(self.request, 'id', 'GET')

    def get(self):
        try:
            queryset = Ostype.objects.all()
            if self.id:
                query_conditions = {'ostypeid': self.id}
                queryset = Ostype.objects.filter(**query_conditions)
            serializer = OstypeSerializer(queryset, many=True)
            return api_return(message={constants.STATUS: constants.TRUE, constants.MESSAGE: constants.SUCCESS},
                              data=serializer.data)
        except Exception, e:
            print traceback.format_exc(e)
            return exception_handler(e)

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
