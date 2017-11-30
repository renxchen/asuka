from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    name = models.CharField(max_length=32, blank=True)
    password = models.CharField(max_length=32, blank=True)
    token = models.CharField(max_length=500, blank=True)
    mail = models.CharField(max_length=200, blank=True)

class Triggers(models.Model):
    triggerId = models.IntegerField(primary_key=True)
    expression = models.CharField(max_length=255)
    descr = models.CharField(max_length=255)
    status = models.IntegerField()
    value = models.IntegerField()
    priority = models.IntegerField()
    lastchange = models.IntegerField()

    class Meta:
        db_table = "Triggers"