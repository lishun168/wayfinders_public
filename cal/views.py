from django.shortcuts import render
from django.utils.safestring import mark_safe
from datetime import datetime
from django.views import View
from datetime import date
from calendar import HTMLCalendar
from itertools import groupby
from .models import Calendar as CalendarModel, Event, Filter
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators import csrf
from django.views.generic.edit import CreateView, UpdateView
from django.forms.widgets import SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget
from django.utils.html import conditional_escape as esc



import logging
logger = logging.getLogger(__name__)

class EventCalendar(HTMLCalendar):

    def __init__(self, events):
        super(EventCalendar, self).__init__()
        self.events = self.group_by_day(events)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            cssclass += ' day'
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.events:
                cssclass += ' filled'
                body = ['<div>']
                for event in self.events[day]:
                    event_link = '/event/' + str(event.pk)
                    event_html = '<a href=' + event_link + '>'
                    body.append('<div>')
                    body.append(event_html)
                    body.append(esc(event.name))
                    body.append('</a></div>')
                body.append('</div>')
                return self.day_cell(cssclass, '%d %s' % (day, '<br>'.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(EventCalendar, self).formatmonth(year, month)

    def group_by_day(self, events):
        field = lambda event: event.date.day
        return dict(
            [(day, list(items)) for day, items in groupby(events, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)

class Calendar(View):
    template_name = 'cal/calendar.html'

    def get(self, request, pk):

        c = CalendarModel.objects.get(pk=pk)
        f = Filter.objects.filter(calendar=c)
        today = datetime.today()
        tomorrow = datetime(today.year, today.month, today.day + 1)
        times = [
            "12 AM",
            "1 AM",
            "2 AM",
            "3 AM",
            "4 AM",
            "5 AM",
            "6 AM",
            "7 AM",
            "8 AM",
            "9 AM",
            "10 AM",
            "11 AM",
            "12 PM",
            "1 PM",
            "2 PM",
            "3 PM",
            "4 PM",
            "5 PM",
            "6 PM",
            "7 PM",
            "8 PM",
            "9 PM",
            "10 PM",
            "11 PM"
        ]
        
        events = Event.objects.all()
        html_c = EventCalendar(events).formatmonth(today.year, today.month)

        context = {
            'month': today.month,
            'year': today.year,
            'day': today.day,
            'week': today.weekday,
            'calendar': c,
            'html_calendar': mark_safe(html_c),
            'times': times,
            'filters': f
        }

        return render(request, self.template_name, context)

class CreateEvent(CreateView):
    template_name = 'cal/create_event.html'
    model = Event
    fields = ('name', 'description', 'date', 'time', 'end_time', 'public', 'calendar_filter')

    def get_form(self):
        today = datetime.today()
        form = super(CreateEvent, self).get_form()
        return form


    def dispatch(self, *args, **kwargs):
        return super(CreateEvent, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        logger.error("form_valid")
        obj = form.save(commit=False)
        cal_pk = self.kwargs.get('pk')
        cal = CalendarModel.objects.get(pk=cal_pk)
        obj.calendar = cal
        logger.error(obj)
        obj.save() 

        success_url = "/calendar/" + str(cal_pk)
        return HttpResponseRedirect(success_url)

class UpdateEvent(UpdateView):
    template_name = 'cal/update_event.html'
    model = Event
    fields = ('name', 'description', 'date', 'time', 'end_time', 'public', 'calendar_filter')
    success_url = "/"

    def dispatch(self, *args, **kwargs):
        return super(UpdateEvent, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        event_pk = self.kwargs.get('event_pk')
        obj.save()

        success_url = "/calendar/" + str(self.object.calendar.id)
        return HttpResponseRedirect(success_url)

class ViewEvent(View):
    template_name = 'cal/event.html'
    
    def get(self, request, pk):
        eve = Event.objects.get(pk=pk)

        context = {
            'event': eve
        }

        return render(request, self.template_name, context)

class CreateFilter(CreateView):
    template_name = 'cal/create_filter.html'
    model = Filter
    fields = ('name',)

    def dispatch(self, *args, **kwargs):
        return super(CreateFilter, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        cal_pk = self.kwargs.get('pk')
        cal = CalendarModel.objects.get(pk=cal_pk)
        obj.calendar = cal
        logger.error(obj)
        obj.save() 

        success_url = "/calendar/" + str(cal_pk)
        return HttpResponseRedirect(success_url)
    

@csrf.csrf_exempt
def create_event(request):
   
    return HttpResponse('success')
