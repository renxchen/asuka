#!/usr/bin/env python
# coding=utf-8

'''

@author: necwang
@contact: necwang@cisco.com
@file: collection_policy_views.py
@time: 2017/12/14 14:39
@desc:

'''

from backend.apolo.serializer.collection_policy_serializer import CollPolicyGroupSerializer, PolicyGroupSerializer
from backend.apolo.models import CollPolicyGroups, PolicysGroups, Schedules
from rest_framework import viewsets
from django.core.paginator import Paginator
from backend.apolo.tools.exception import exception_handler
from backend.apolo.tools.views_helper import api_return
from backend.apolo.tools import constants
from backend.apolo.tools import views_helper
import traceback
import time
from django.db import transaction
import simplejson as json
import requests
from django.db.models import Q


class CollPolicyGroupViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(CollPolicyGroupViewSet, self).__init__(**kwargs)
        self.request = request
        method = 'GET'
        if request.method.lower() == 'get' or request.method.lower() == 'delete':
            method = 'GET'
        if request.method.lower() == 'post' or request.method.lower() == 'put':
            method = 'BODY'
        self.new_token = views_helper.get_request_value(self.request, "NEW_TOKEN", 'META')
        self.page_from = views_helper.get_request_value(self.request, 'page', 'GET')
        self.max_size_per_page = views_helper.get_request_value(self.request, 'rows', 'GET')
        self.id = views_helper.get_request_value(self.request, 'id', method)
        self.name = views_helper.get_request_value(self.request, 'name', method)
        self.desc = views_helper.get_request_value(self.request, 'desc', method)
        self.ostype = views_helper.get_request_value(self.request, 'ostype_name', method)
        self.ostype_for_search = views_helper.get_request_value(self.request, 'ostypeid__name', method)
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
    def get_cp_group(**kwargs):
        """!@brief
        Get the data of CollPolicyGroups table
        @param kwargs: dictionary type of the query condition
        @pre call when need data of CollPolicyGroups table
        @post return CollPolicyGroups data
        @return: data of CollPolicyGroups table
        """
        try:
            cpg = CollPolicyGroups.objects.get(**kwargs)
            return cpg
        except Exception, e:
            return False

    @staticmethod
    def get_policy_group(**kwargs):
        """!@brief
        Get the data of PolicysGroups table
        @param kwargs: dictionary type of the query condition
        @pre call when need data of PolicysGroups table
        @post return PolicysGroups data
        @return: data of PolicysGroups table
        """
        try:
            pg = PolicysGroups.objects.filter(**kwargs)
            return pg
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    @staticmethod
    def get_schedule(**kwargs):
        """!@brief
        Get the data of Schedules table
        @param kwargs: dictionary type of the query condition
        @pre call when need data of Schedules table
        @post return Schedules data
        @return: data of Schedules table
        """
        try:
            return Schedules.objects.filter(**kwargs)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    @staticmethod
    def get_policys_groups(**kwargs):
        """!@brief
        Get the data of PolicysGroups table
        @param kwargs: dictionary type of the query condition
        @pre call when need data of PolicysGroups table
        @post return PolicysGroups data
        @return: data of PolicysGroups table
        """
        try:
            policys_groups = PolicysGroups.objects.get(**kwargs)
            return policys_groups
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return False

    def del_policy_group_and_coll_policy_group(self, **kwargs):
        """!@brief
        Delete policys_groups and coll_policy_group
        @param kwargs: dictionary type of the query condition
        @pre call when need to delete policys_groups and coll_policy_group
        @return: status
        """
        try:
            queryset = self.get_cp_group(**kwargs)
            if queryset is False:
                data = {
                    constants.STATUS: {
                        constants.STATUS: constants.FALSE,
                        constants.MESSAGE: constants.COLL_POLICY_GROUP_NOT_FOUND
                    }
                }
                return data
            pgs = self.get_policy_group(**kwargs)
            if isinstance(pgs, str):
                if json.loads(pgs)['message'] is not '':
                    data = {
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: json.loads(pgs)['message']
                        }
                    }
                    return data
            pgs.delete()
            queryset.delete()
            return True
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def del_policy_group(self, **kwargs):
        """!@brief
        Delete policys_groups and coll_policy_group
        @param kwargs: dictionary type of the query condition
        @pre call when need to delete policys_groups
        @return: status
        """
        try:
            pgs = self.get_policy_group(**kwargs)
            # if len(pgs) > 0:
            pgs.delete()
            # return True
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def verify_column_bak(self, id, method='GET'):
        """!@brief
        Return the status of each column, decide whether should disable or enable in web page
        False: modify reject, True: modify or shown permit
        @param id: policy group id
        @param method: request method, default is GET
        @pre call when need to get the column status
        @post return column status
        @return verify_result: the status of each column
        """
        try:
            self.get_execute_ing()
            if id is not '':
                queryset_pg = PolicysGroups.objects.filter(**{'policy_group_id': id})
                verify_result = {
                    'desc': True,
                    'status': True,
                    'ostype': True,
                    'collection_policy_name': True,
                    'collection_policy_group_name': True,
                    'exec_interval': True,
                    'execute_ing': self.execute_ing,
                }
                if len(queryset_pg) > 0 or self.execute_ing:
                    verify_result['ostype'] = False
                if self.execute_ing:
                    verify_result['collection_policy_name'] = False
                    verify_result['exec_interval'] = False
                return verify_result
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    @staticmethod
    def verify_column(id, method='GET'):
        """!@brief
        Return the status decide whether cpg can be modified
        False: modify reject, True: modify allow
        @param id: policy group id
        @param method: request method, default is GET
        @pre call when need to get the column status
        @post return column status
        @return verify_result: status
        """
        try:
            if id is not '':
                queryset_pg = Schedules.objects.filter(**{'policy_group_id': id})
                verify_result = {
                    'status': True,
                }
                if len(queryset_pg) > 0:
                    verify_result['status'] = False
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
                queryset = CollPolicyGroups.objects.filter(**{'policy_group_id': self.id})
                queryset_pg = PolicysGroups.objects.filter(**{'policy_group_id': self.id})
                serializer = CollPolicyGroupSerializer(queryset, many=True)
                serializer_pg = PolicyGroupSerializer(queryset_pg, many=True)
                for per in serializer_pg.data:
                    if per['policy_policy_type'] == constants.NUMBER_ONE:
                        # SNMP
                        per['policy_name'] = '[SNMP]' + per['policy_name']
                    else:
                        # CLI
                        per['policy_name'] = '[CLI]' + per['policy_name']
                verify_result = self.verify_column(self.id)
                data = {
                    'data': {
                        'policys_groups_data': serializer_pg.data,
                        'policy_group_data': serializer.data,
                        'verify_result': verify_result,
                    },
                    'new_token': self.new_token,
                    constants.STATUS: {
                        constants.STATUS: constants.TRUE,
                        constants.MESSAGE: constants.SUCCESS,
                    },
                }
                # verify_result = self.get_schedule(**{'policy_group_id': self.id})
                # if verify_result is False:
                #     data[constants.STATUS][constants.MESSAGE] = constants.COLL_POLICY_GROUP_EXIST_IN_SCHEDULE
                return api_return(data=data)
            field_relation_ships = {
                'id': 'policy_group_id',
                'name': 'name',
                'desc': 'desc',
                'ostypeid__name': 'ostypeid__name',
            }
            query_data = {
                'name': self.name,
                'desc': self.desc,
                'ostypeid__name': self.ostype_for_search,
            }
            search_fields = ['name', 'ostypeid__name', 'desc']
            sorts, search_conditions = views_helper.get_search_conditions(self.request, field_relation_ships,
                                                                          query_data, search_fields)
            total_num = len(CollPolicyGroups.objects.all())
            if search_conditions:
                queryset = CollPolicyGroups.objects.filter(**search_conditions).values(
                    *['policy_group_id', 'ostypeid', 'name', 'desc', 'ostypeid__name']).order_by(*sorts)
            else:
                queryset = CollPolicyGroups.objects.all().values(
                    *['policy_group_id', 'ostypeid', 'name', 'desc', 'ostypeid__name']).order_by(*sorts)
            # serializer = CollPolicyGroupSerializer(queryset, many=True)
            paginator = Paginator(list(queryset), self.max_size_per_page)
            contacts = paginator.page(self.page_from)
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
        Create policy group
        @return data: the status of whether create successful and the inserted data
        """
        try:
            with transaction.atomic():
                data = {
                    'name': self.name,
                    'desc': self.desc,
                    'ostypeid': self.ostype,
                }
                if self.name is not '':
                    get_name_from_cpg = self.get_cp_group(**{'name': self.name})
                    if get_name_from_cpg is not False:
                        data = {
                            constants.STATUS: {
                                constants.STATUS: constants.FALSE,
                                constants.MSG_TYPE: 'NAME_DUPLICATE',
                                constants.MESSAGE: constants.COLLECTION_POLICY_GROUP_NAME_DUPLICATE
                            }
                        }
                        return api_return(data=data)
                cps = views_helper.get_request_value(self.request, 'cps', 'BODY')
                serializer = CollPolicyGroupSerializer(data=data)
                if serializer.is_valid(Exception):
                    serializer.save()
                    policy_group_data = []
                    for per_cp in cps:
                        per_cp['policy_group'] = int(serializer.data.get('policy_group_id'))
                        per_cp['history'] = time.time()
                        per_cp['policy'] = per_cp['policy']
                        policy_group_data.append(per_cp)
                    serializer_related = PolicyGroupSerializer(data=policy_group_data, many=True)
                    if serializer_related.is_valid(Exception):
                        serializer_related.save()
                    data = {
                        'data': {
                            'data_coll_policy': serializer.data,
                            'data_policys_groups': serializer_related.data,
                        },
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.TRUE,
                            constants.MESSAGE: constants.POST_SUCCESSFUL
                        }
                    }
                    return api_return(data=data)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    def put(self):
        """!@brief
        Modify policy group data
        @return data: the status of whether modified successful and the modified data
        """
        try:
            # self.get_execute_ing()
            kwargs = {'policy_group_id': self.id}
            cps = views_helper.get_request_value(self.request, 'cps', 'BODY')
            with transaction.atomic():
                queryset = self.get_cp_group(**kwargs)
                if queryset is False:
                    data = {
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.COLL_POLICY_GROUP_NOT_FOUND
                        }
                    }
                    return api_return(data=data)
                data = {
                    'policy_group_id': int(self.id),
                    'name': self.name,
                    'desc': self.desc,
                    'ostypeid': self.ostype,
                }
                # if self.name is not '':
                #     get_name_from_cpg = self.get_cp_group(**{'name': self.name})
                #     if get_name_from_cpg is not False:
                #         data = {
                #             constants.STATUS: {
                #                 constants.STATUS: constants.FALSE,
                #                 constants.MESSAGE: constants.COLLECTION_POLICY_GROUP_NAME_DUPLICATE
                #             }
                #         }
                #         return api_return(data=data)
                if len(CollPolicyGroups.objects.filter(~Q(policy_group_id=self.id), name=self.name)):
                    data = {
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MSG_TYPE: 'NAME_DUPLICATE',
                            constants.MESSAGE: constants.COLLECTION_POLICY_GROUP_NAME_DUPLICATE
                        }
                    }
                    return api_return(data=data)
                # collection policy group is running, just name, desc and on/off in table can modify.
                verify_result = self.verify_column(self.id)
                if not verify_result['status']:
                    serializer = CollPolicyGroupSerializer(queryset, data=data)
                    if serializer.is_valid(Exception):
                        serializer.save()
                        policy_group_data = []
                        for per_cp in cps:
                            per_cp['history'] = time.time()
                            policy_group_data_queryset = self.get_policys_groups(
                                **{'policys_groups_id': per_cp['policys_groups_id']})
                            # policy_group_data.append(policy_group_data_queryset)
                            serializer_related = PolicyGroupSerializer(policy_group_data_queryset, data=per_cp)
                            if serializer_related.is_valid(Exception):
                                serializer_related.save()
                            policy_group_data.append(serializer_related.data)
                        data = {
                            'data': {
                                'data_coll_policy': serializer.data,
                                'data_policys_groups': policy_group_data,
                            },
                            'new_token': self.new_token,
                            constants.STATUS: {
                                constants.STATUS: constants.TRUE,
                                constants.MESSAGE: constants.PUT_SUCCESSFUL
                            }
                        }
                        return api_return(data=data)
                # collection policy group not exist in schedule, cpg name, cpg desc, cpg ostype and all the data in table can modify
                else:
                    self.del_policy_group(**kwargs)
                    # if result is True:
                    serializer = CollPolicyGroupSerializer(queryset, data=data)
                    if serializer.is_valid(Exception):
                        serializer.save()
                        policy_group_data = []
                        for per_cp in cps:
                            per_cp['policy_group'] = int(serializer.data.get('policy_group_id'))
                            per_cp['history'] = time.time()
                            per_cp['policy'] = per_cp['policy']
                            policy_group_data.append(per_cp)
                        serializer_related = PolicyGroupSerializer(data=policy_group_data, many=True)
                        if serializer_related.is_valid(Exception):
                            serializer_related.save()
                        data = {
                            'data': {
                                'data_coll_policy': serializer.data,
                                'data_policys_groups': serializer_related.data,
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
        Delete policy group data
        @return data: the status of whether deleted successful
        """
        try:
            # self.get_execute_ing()
            with transaction.atomic():
                kwargs = {'policy_group_id': self.id}
                verify_result = self.verify_column(self.id)
                if not verify_result['status']:
                    data = {
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.COLL_POLICY_GROUP_EXIST_IN_SCHEDULE
                        }
                    }
                    return api_return(data=data)
                data = self.del_policy_group_and_coll_policy_group(**kwargs)
                if data is True:
                    data = {
                        'new_token': self.new_token,
                        constants.STATUS: {
                            constants.STATUS: constants.TRUE,
                            constants.MESSAGE: constants.DELETE_SUCCESSFUL
                        }
                    }
                return api_return(data=data)
        except Exception, e:
            transaction.rollback()
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)
