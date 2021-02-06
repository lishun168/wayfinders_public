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


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(u'Description', blank=True, null=True)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    date = models.DateField(u'Day of Event', default=datetime.now)
    time = models.TimeField(u'Starting time', default=datetime.now)
    end_time = models.TimeField(u'Final time', default=datetime.now)
    calendar_filter = models.ForeignKey(Filter, on_delete = models.SET_NULL, null=True, blank=True) 
    public = models.BooleanField(default=True)

    def __str__(self):
        return '%s - %s' % (self.calendar, self.name)

    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap=False
        if new_start == fixed_end or new_end == fixed_start:
            overlap=False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (new_end >= fixed_start and new_end <= fixed_end):
            overlap=True
        elif new_start <= fixed_start and new_end >= fixed_end:
            overlap=True
        
        return overlap

    def get_absolute_url(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, str(self.time))

class Invitation(models.Model):
    pending = models.BooleanField(default=True)
    accepted = models.BooleanField(default=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.event, self.member)
