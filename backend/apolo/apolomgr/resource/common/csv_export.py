#!/usr/bin/env python
# coding=utf-8
"""

@author: necwang
@contact: necwang@cisco.com
@file: csv_export.py
@time: 2018/3/9 10:55
@desc:

"""
import codecs
import csv
import sys
import urllib2

from backend.apolo.tools import constants
import traceback
from backend.apolo.tools.exception import exception_handler
from django.http import StreamingHttpResponse
import os


def csv_export(file_path, data):
    try:
        if sys.version_info >= (3, 0, 0):
            f = open(file_path, 'w', newline='')
        else:
            f = open(file_path, 'wb')
        # resolve the issue of encode of Chinese or Japanese
        f.write(codecs.BOM_UTF8)
        writer = csv.writer(f)
        for i in range(len(data)):
            writer.writerow(data[i])
        f.close()
        if os.path.exists(file_path):
            # download csv
            return output_down_load(file_path)
        else:
            return False
    except Exception, e:
        if constants.DEBUG_FLAG:
            print traceback.format_exc(e)
        return exception_handler(e)


def output_down_load(path):
    def file_iterator2(path, chunk_size=512):
        with open(path) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    try:
        response = StreamingHttpResponse(file_iterator2(path))
        response['Content-Type'] = 'application/octet-stream'
        file_name = path.split('/')[-1]
        response['Content-Disposition'] = 'attachment;filename=' + file_name
        return response
    except Exception, e:
        print e
