from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    name = models.CharField(max_length=32, blank=True)
    password = models.CharField(max_length=32, blank=True)
    token = models.CharField(max_length=500, blank=True)
    mail = models.CharField(max_length=200, blank=True)
