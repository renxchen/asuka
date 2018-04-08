#!/usr/bin/env python

'''

@author: necwang
@contact: necwang@cisco.com
@file: db_until.py.py
@time: 2018/1/4 16:57
@desc:

'''
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.server.settings")
django.setup()