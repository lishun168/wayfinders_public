from django.db import models
from members.models import Member
from cal.models import Calendar, Filter
from datetime import datetime

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(u'Description', blank=True, null=True)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    date = models.DateField(u'Day of Event', default=datetime.now)
    time = models.TimeField(u'Start Time', default=datetime.now)
    end_time = models.TimeField(u'End Time', default=datetime.now)
    sub_calendar = models.ForeignKey(Filter, on_delete=models.SET_NULL, null=True, blank=True)
    public = models.BooleanField(default=True)
    is_open = models.BooleanField(default=False)
    open_editing = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' % (self.calendar, self.name)

    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:
            overlap = False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (new_end >= fixed_start and new_end <= fixed_end):
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end:
            overlap = True

        return overlap

    def get_absolute_url(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, str(self.time))

class Invitation(models.Model):
    member=models.ForeignKey(Member,on_delete=models.CASCADE) #choose the member
    events=models.ForeignKey(Event,on_delete=models.CASCADE) #pull the id of the event
    accept=models.BooleanField(default=False)
    decline=models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' % (self.events, self.member)

class Participants(models.Model):
    member=models.ForeignKey(Member,on_delete=models.CASCADE)
    events=models.ForeignKey(Event,on_delete=models.CASCADE)
    is_administrator = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' % (self.events, self.member)

    class Meta:
        verbose_name='Participant'
        verbose_name_plural='Participants'

