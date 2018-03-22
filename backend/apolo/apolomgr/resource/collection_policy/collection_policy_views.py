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
        # verify whether is executing status
        # self.get_execute_ing()

    def get_execute_ing(self):
        """!@brief
        Get the status of whether is executing or not
        @pre call the api from Gin
        @post return the status
        @return execute_ing: status
        """
        # {
        #     "now_time": 1513312116,
        #     "param": 2,
        #     "param_type": 0  # 0: group 1: policy
        # }
        try:
            req_body = {'now_time': time.time(), 'param': self.id, 'param_type': 0}
            url = constants.VERIFY_WHETHER_EXECUTING_SERVER_URL % (
                constants.VERIFY_WHETHER_EXECUTING_SERVER_IP, constants.VERIFY_WHETHER_EXECUTING_SERVER_PORT)
            headers = {'content-type': 'application/json'}
            resp = requests.post(url=url, data=json.dumps(req_body), headers=headers)
            if 200 <= resp.status_code <= 299:
                resp_body = json.loads(resp.text)
                item = resp_body.get('items')
                if item == constants.NUMBER_ZERO:
                    self.execute_ing = False
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    @staticmethod
    def get_cp(**kwargs):
        """!@brief
        Get the data of CollPolicy table
        @param kwargs: dictionary type of the query condition
        @pre call when need data of CollPolicy table
        @post return CollPolicy data
        @return: data of CollPolicy table
        """
        try:
            return CollPolicy.objects.get(**kwargs)
        except CollPolicy.DoesNotExist:
            return False

    @staticmethod
    def get_cp_from_item(**kwargs):
        """!@brief
        Get the data of Items table
        @param kwargs: dictionary type of the query condition
        @pre call when need data of Items table
        @post return Items data
        @return: data of Items table
        """
        try:
            return Items.objects.filter(**kwargs)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return False

    @staticmethod
    def get_cp_from_policys_groups(**kwargs):
        """!@brief
        Get the data of PolicysGroups table
        @param kwargs: dictionary type of the query condition
        @pre call when need data of PolicysGroups table
        @post return PolicysGroups data
        @return: data of PolicysGroups table
        """
        try:
            return PolicysGroups.objects.filter(**kwargs)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return False

    @staticmethod
    def get_tree_from_coll_policy_rule_tree(**kwargs):
        """!@brief
        Get the data of CollPolicyRuleTree table
        @param kwargs: dictionary type of the query condition
        @pre call when need data of CollPolicyRuleTree table
        @post return CollPolicyRuleTree data
        @return: data of CollPolicyRuleTree table
        """
        try:
            return CollPolicyRuleTree.objects.filter(**kwargs)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return False

    @staticmethod
    def get_tree_from_coll_policy_cli_rule(**kwargs):
        """!@brief
        Get the data of CollPolicyCliRule table
        @param kwargs: dictionary type of the query condition
        @pre call when need data of CollPolicyCliRule table
        @post return CollPolicyCliRule data
        @return: data of CollPolicyCliRule table
        """
        try:
            return CollPolicyCliRule.objects.filter(**kwargs)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return False

    def verify_column(self, id, method='GET'):
        """!@brief
        Return the status of each column, decide whether should disable or enable in web page
        False: modify reject, True: modify or shown permit
        @param id: collection policy id
        @param method: request method, default is GET
        @pre call when need to get the column status
        @post return column status
        @return verify_result: the status of each column
        """
        try:
            self.get_execute_ing()
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
        """!@brief
        Return the data for summary page or return the data for [表示] button
        @return data: data for summary page or data for [表示] button
        """
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
                queryset = CollPolicy.objects.filter(**search_conditions).values(
                    *['coll_policy_id', 'ostype', 'name', 'cli_command', 'desc', 'snmp_oid', 'value_type',
                      'policy_type', 'ostype__name']).order_by(*sorts)
            else:
                queryset = CollPolicy.objects.filter(**{'policy_type': self.policy_type}).values(
                    *['coll_policy_id', 'ostype', 'name', 'cli_command', 'desc', 'snmp_oid', 'value_type',
                      'policy_type', 'ostype__name']).order_by(*sorts)
            # serializer = CollPolicySerializer(queryset, many=True)
            paginator = Paginator(list(queryset), int(self.max_size_per_page))
            contacts = paginator.page(int(self.page_from))
            data = {
                'data': {
                    'data': contacts.object_list,
                },
                'new_token': self.new_token,
                'num_page': paginator.num_pages,
                # 'page_range': list(paginator.page_range),
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
        """!@brief
        Create collection policy
        @return data: the status of whether create successful and the inserted data
        """
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
                if int(self.policy_type) == constants.NUMBER_ONE:
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
        """!@brief
        Modify collection policy data
        @return data: the status of whether modified successful and the modified data
        """
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
                    data = {
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.COLLECTION_POLICY_NOT_EXIST % self.id
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
        """!@brief
        Delete collection policy data
        @return data: the status of whether deleted successful
        """
        try:
            self.get_execute_ing()
            with transaction.atomic():
                kwargs = {'coll_policy_id': self.id}
                collection_policy_in_cp = self.get_cp(**kwargs)
                cp_rule_tree = self.get_tree_from_coll_policy_rule_tree(**kwargs)
                cp_cli_rule = self.get_tree_from_coll_policy_cli_rule(**kwargs)
                pg = self.get_cp_from_policys_groups(**{'policy_id': self.id})
                if self.execute_ing:
                    data = {
                        'data': {
                            'data': constants.COLLECTION_POLICY_IS_EXECUTING % self.id
                        },
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.COLL_POLICY_EXIST_IN_POLICYS_GROUPS
                        }
                    }
                    return api_return(data=data)
                if collection_policy_in_cp is False:
                    data = {
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.COLLECTION_POLICY_NOT_EXIST % self.id
                        }
                    }
                    return api_return(data=data)
                if len(pg) > 0:
                    data = {
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
