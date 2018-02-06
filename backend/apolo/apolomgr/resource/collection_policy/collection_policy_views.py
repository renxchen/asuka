# encoding=utf-8
# !/usr/bin/env python

"""

@author: kimli
@contact: kimli@cisco.com
@file: collection_policy_views.py
@time: 2017/12/14 14:39
@desc:

"""
from backend.apolo.serializer.collection_policy_serializer import CollPolicySerializer
from backend.apolo.models import CollPolicy, Items, PolicysGroups, CollPolicyGroups, CollPolicyRuleTree, \
    CollPolicyCliRule
from rest_framework import viewsets
from django.utils.translation import gettext
from django.core.paginator import Paginator
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return
from backend.apolo.tools import constants
from backend.apolo.tools import views_helper
import traceback
from backend.apolo.apolomgr.resource.common.common_policy_tree.policy_tree import Policy_tree
from django.db import transaction
import time
import requests
import simplejson as json


class CollPolicyViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(CollPolicyViewSet, self).__init__(**kwargs)
        self.request = request
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        self.page_from = views_helper.get_request_value(self.request, 'page', 'GET')
        self.max_size_per_page = views_helper.get_request_value(self.request, 'rows', 'GET')
        method = 'GET'
        if request.method.lower() == 'get' or request.method.lower() == 'delete':
            method = 'GET'
        if request.method.lower() == 'post' or request.method.lower() == 'put':
            method = 'BODY'
        self.policy_type = views_helper.get_request_value(self.request, 'policy_type', method)
        self.id = views_helper.get_request_value(self.request, 'id', method)
        self.name = views_helper.get_request_value(self.request, 'name', method)
        self.ostype = views_helper.get_request_value(self.request, 'ostype', method)
        self.cli_command = views_helper.get_request_value(self.request, 'cli_command', method)
        self.desc = views_helper.get_request_value(self.request, 'desc', method)
        self.snmp_oid = views_helper.get_request_value(self.request, 'snmp_oid', method)
        self.value_type = views_helper.get_request_value(self.request, 'value_type', method)
        self.execute_ing = True
        # verify execute_ing status
        self.get_execute_ing()

    def get_execute_ing(self):
        # {
        #     "now_time": 1513312116,
        #     "param": 2,
        #     "param_type": 0  # 0: group 1: policy
        # }
        req_body = {'now_time': time.time(), 'param': self.id, 'param_type': 0}
        url = "http://%s:%s/api/v1/valid" % ('10.71.244.134', '7777')
        headers = {'content-type': 'application/json'}
        resp = requests.post(url=url, data=json.dumps(req_body), headers=headers)
        if 200 <= resp.status_code <= 299:
            resp_body = json.loads(resp.text)
            item = resp_body.get('items')
            if item == 0:
                self.execute_ing = False

    @staticmethod
    def get_cp(**kwargs):
        try:
            return CollPolicy.objects.get(**kwargs)
        except CollPolicy.DoesNotExist:
            return False

    @staticmethod
    def get_cp_from_item(**kwargs):
        try:
            return Items.objects.filter(**kwargs)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return False

    @staticmethod
    def get_cp_from_policys_groups(**kwargs):
        try:
            return PolicysGroups.objects.filter(**kwargs)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return False

    @staticmethod
    def get_tree_from_coll_policy_rule_tree(**kwargs):
        try:
            return CollPolicyRuleTree.objects.filter(**kwargs)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return False

    @staticmethod
    def get_tree_from_coll_policy_cli_rule(**kwargs):
        try:
            return CollPolicyCliRule.objects.filter(**kwargs)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return False

    def verify_column(self, id, method='GET'):
        """
        verify column
        :return: False: modify reject, True: modify or shown permit
        """
        try:
            if id is not '':
                cp = CollPolicy.objects.get(coll_policy_id=int(id))
                cpg = CollPolicyGroups.objects.filter(**{'ostypeid': int(cp.ostype_id)})
                verify_result = {
                    'ostype': True,
                    'snmp_oid': True,
                    'execute_ing': self.execute_ing,
                }
                if len(cpg) > 0:
                    verify_result['ostype'] = False
                if self.execute_ing:
                    verify_result['snmp_oid'] = False
                return verify_result
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def get(self):
        try:
            if self.id is not '':
                queryset = CollPolicy.objects.filter(**{'coll_policy_id': self.id})
                verify_result = self.verify_column(self.id)
                serializer = CollPolicySerializer(queryset, many=True)
                # get tree information
                pt_data = {}
                pt = Policy_tree(self.id)
                try:
                    pt_data = pt.get_policy_tree()
                except Exception, e:
                    if constants.DEBUG_FLAG:
                        print traceback.format_exc(e)
                    exception_handler(e)
                data = {
                    'data': {
                        'data': serializer.data,
                        'verify_result': verify_result,
                    },
                    'new_token': self.new_token,
                    constants.STATUS: {
                        constants.STATUS: constants.TRUE,
                        constants.MESSAGE: constants.SUCCESS
                    },
                    'policy_tree': pt_data,
                }
                return api_return(data=data)
            field_relation_ships = {
                'id': 'id',
                'name': 'name',
                'desc': 'desc',
                'cli_command': 'cli_command',
                'ostype': 'ostype__name',
                'snmp_oid': 'snmp_oid',
                'policy_type': 'policy_type',
            }
            query_data = {
                'name': self.name,
                'desc': self.desc,
                'cli_command': self.cli_command,
                'ostype__name': self.ostype,
                'snmp_oid': self.snmp_oid,
                'policy_type': self.policy_type,
            }
            search_fields = ['name', 'ostype', 'cli_command', 'desc', 'snmp_oid']
            sorts, search_conditions = views_helper.get_search_conditions(self.request, field_relation_ships,
                                                                          query_data, search_fields)
            total_num = len(CollPolicy.objects.filter(**{'policy_type': self.policy_type}))
            if search_conditions:
                queryset = CollPolicy.objects.filter(**search_conditions).order_by(*sorts)
            else:
                queryset = CollPolicy.objects.filter(**{'policy_type': self.policy_type}).order_by(*sorts)
            serializer = CollPolicySerializer(queryset, many=True)
            paginator = Paginator(serializer.data, int(self.max_size_per_page))
            contacts = paginator.page(int(self.page_from))
            data = {
                'data': {
                    'data': contacts.object_list,
                },
                'new_token': self.new_token,
                'num_page': paginator.num_pages,
                'page_range': list(paginator.page_range),
                'page_has_next': contacts.has_next(),
                'total_num': total_num,
                'current_page_num': contacts.number,
                constants.STATUS: {
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.SUCCESS
                },
            }
            return api_return(data=data)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def post(self):
        try:
            with transaction.atomic():
                data = {
                    'name': self.name,
                    'desc': self.desc,
                    'cli_command': self.cli_command,
                    'ostype': self.ostype,
                    'snmp_oid': self.snmp_oid,
                    'policy_type': self.policy_type,
                }
                if self.name is not '':
                    get_name_from_cp = self.get_cp(**{'name': self.name})
                    if get_name_from_cp is not False:
                        data = {
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MESSAGE: constants.COLLECTION_POLICY_NAME_DUPLICATE
                            }
                        }
                        return api_return(data=data)
                if int(self.policy_type) == 1:
                    data['value_type'] = self.value_type
                serializer = CollPolicySerializer(data=data)
                if serializer.is_valid(Exception):
                    serializer.save()
                    data = {
                        'data': {
                            'data': serializer.data,
                        },
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.TRUE,
                            constants.MESSAGE: constants.SUCCESS
                        }
                    }
                    return api_return(data=data)
        except Exception, e:
            transaction.rollback()
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def put(self):
        try:
            with transaction.atomic():
                kwargs = {'coll_policy_id': self.id}
                queryset = self.get_cp(**kwargs)
                data = {
                    'name': self.name,
                    'desc': self.desc,
                    'ostype': self.ostype,
                    'snmp_oid': self.snmp_oid,
                    'value_type': self.value_type,
                }
                if queryset is False:
                    message = 'There is no result in CollPolicy table with id %s.' % self.id
                    data = {
                        'data': {
                            'data': message
                        },
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.FAILED
                        }
                    }
                    return api_return(data=data)
                serializer = CollPolicySerializer(queryset, data=data)
                if serializer.is_valid(Exception):
                    serializer.save()
                    data = {
                        'data': {
                            'data': serializer.data,
                        },
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.TRUE,
                            constants.MESSAGE: constants.SUCCESS
                        }
                    }
                    return api_return(data=data)
        except Exception, e:
            transaction.rollback()
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def delete(self):
        try:
            with transaction.atomic():
                kwargs = {'coll_policy_id': self.id}
                collection_policy_in_cp = self.get_cp(**kwargs)
                cp_rule_tree = self.get_tree_from_coll_policy_rule_tree(**kwargs)
                cp_cli_rule = self.get_tree_from_coll_policy_cli_rule(**kwargs)
                pg = self.get_cp_from_policys_groups(**{'policy_id': self.id})
                if self.execute_ing:
                    message = 'Collection policy is running in system with id %s.' % self.id
                    data = {
                        'data': {
                            'data': message
                        },
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.COLL_POLICY_EXIST_IN_POLICYS_GROUPS
                        }
                    }
                    return api_return(data=data)
                if collection_policy_in_cp is False:
                    message = 'There is no result in CollPolicy table with id %s.' % self.id
                    data = {
                        'data': {
                            'data': message
                        },
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.FAILED
                        }
                    }
                    return api_return(data=data)
                if len(pg) > 0:
                    message = 'Collection policy exists in PolicysGroups table with id %s.' % self.id
                    data = {
                        'data': {
                            'data': message
                        },
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.COLL_POLICY_EXIST_IN_POLICYS_GROUPS
                        }
                    }
                    return api_return(data=data)
                # delete cp in policys_groups table
                pg.delete()
                # delete cp in coll_policy_rule_tree table
                cp_rule_tree.delete()
                # delete cp in coll_policy_cli_rule table
                cp_cli_rule.delete()
                # delete cp in coll_policy table
                collection_policy_in_cp.delete()
                data = {
                    'new_token': self.new_token,
                    constants.STATUS: {
                        constants.STATUS: constants.TRUE,
                        constants.MESSAGE: constants.SUCCESS
                    }
                }
                return api_return(data=data)
        except Exception, e:
            transaction.rollback()
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)
