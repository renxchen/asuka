from __future__ import unicode_literals

from django.db import models

# Create your models here.
class test_table1(models.Model):
    col1 = models.CharField(max_length=200, null=True, blank=True)
    col2 = models.CharField(max_length=200, null=True, blank=True)
    col3 = models.CharField(max_length=200, null=True, blank=True)
