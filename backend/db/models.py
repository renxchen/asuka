from django.db import models


class my_table(models.Model):
    col1 = models.CharField(max_length=200, null=True, blank=True)
