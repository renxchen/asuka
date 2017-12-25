#!/usr/bin/env python

"""

@author: kimli
@contact: kimli@cisco.com
@file: views_helper.py
@time: 2017/12/15 13:37
@desc:

"""
from django.db.models import Q
import traceback
from backend.apolo.tools.exception import exception_handler


def get_query_condition(request, query_data, method_type):
    kwargs = {}
    return kwargs


def get_search_conditions(request, field_relation_ships, query_data):
    sort_by = get_request_value(request, 'sort_by', 'GET')
    order = get_request_value(request, 'order', 'GET')
    search_fields = get_request_value(request, 'search_fields', 'GET')
    search_conditions = {}
    if search_fields:
        for i, value in enumerate(search_fields.split(',')):
            if value in field_relation_ships:
                field = field_relation_ships[value]
                if query_data[field] == '':
                    continue
                # Q(Name__contains=sqlstr) , Q(MUser__username__contains=sqlstr)
                # each_q = Q(value + '__icontains' + '=' + query_data[value])
                # search_conditions.append(each_q)
                search_conditions[field_relation_ships[value] + '__icontains'] = query_data[field]
    sorts = []
    if sort_by:
        if sort_by in field_relation_ships:
            field_sort = field_relation_ships[sort_by]
            if order == 'desc':
                field_sort = '-' + field_sort

            sorts.append(field_sort)
    return sorts, search_conditions


def get_request_value(request, key, method_type):
    try:
        value = ''
        if method_type.strip().upper() == 'GET':
            value = get_request_get(request, key)
        if method_type.strip().upper() == 'POST':
            value = get_request_post(request, key)
        if method_type.strip().upper() == 'META':
            value = get_request_header(request, key)
        if method_type.strip().upper() == 'BODY':
            value = get_request_body(request, key)
        return value
    except Exception, e:
        print traceback.format_exc(e)
        return exception_handler(e)


def get_request_get(request, key):
    if key in request.GET:
        return request.GET[key]
    return ''


def get_request_header(request, key):
    if key in request.META:
        return request.META.get(key)
    return ''


def get_request_post(request, key):
    if key in request.POST:
        return request.POST[key]
    return ''


def get_request_body(request, key):
    body = eval(request.body)
    if key in body:
        return body.get(key)
    return ''
