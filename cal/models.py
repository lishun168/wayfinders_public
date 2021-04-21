from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError
from django.urls import reverse
from members.models import Member, Company

class Calendar(models.Model):
    public = models.BooleanField(default=True)
    name = models.CharField(max_length=255, default='')

    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '%s' % (self.name)

class Filter(models.Model):
    name = models.CharField(max_length=255)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.calendar, self.name)

