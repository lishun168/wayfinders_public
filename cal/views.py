from django.shortcuts import render
from django.utils.safestring import mark_safe
from datetime import datetime
from django.views import View
from datetime import date
from calendar import HTMLCalendar
from itertools import groupby
from .models import Calendar as CalendarModel, Filter
from events.models import Event, Invitation, Participants
from members.models import Member
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators import csrf
from django.views.generic.edit import CreateView, UpdateView
from django.forms.widgets import SelectDateWidget, TimeInput
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

def get_calendar_context(calendar, filt, date):
    times = [
            "12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM",
            "6 AM", "7 AM", "8 AM", "9 AM", "10 AM", "11 AM",
            "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM",
            "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM"
        ]

    events = Event.objects.filter(date__year=date.year, date__month=date.month)
    html_c = EventCalendar(events).formatmonth(date.year, date.month)
    context = {
            'calendar': calendar,
            'html_calendar': mark_safe(html_c),
            'times': times,
            'filters': filt,
            'date_object': date
    }   

    return context

class Calendar(View):
    template_name = 'cal/calendar.html'
    today = datetime.today()

    def get(self, request, pk):

        c = CalendarModel.objects.get(pk=pk)
        f = Filter.objects.filter(calendar=c)
        today = datetime.today()
        context = get_calendar_context(c, f, today)

        return render(request, self.template_name, context)

class CalendarDate(View):
    template_name = 'cal/calendar.html'

    def get(self, request, pk, year, month):
        c = CalendarModel.objects.get(pk=pk)
        f = Filter.objects.filter(calendar=c)
        today = datetime.today()
        new_date = today.replace(year=year, month=month)
        
        context = get_calendar_context(c, f, new_date)

        return render(request, self.template_name, context)

class CreateEvent(CreateView):
    template_name = 'create_edit_model.html'
    model = Event
    fields = ('name', 'description', 'date', 'time', 'end_time', 'public', 'sub_calendar', 'is_open', 'open_editing')

    def get_form(self):
        today = datetime.today()
        form = super(CreateEvent, self).get_form()
        form.fields['date'].widget = SelectDateWidget()
        form.fields['time'].widget = TimeInput(attrs={'type': 'time'})
        form.fields['end_time'].widget = TimeInput(attrs={'type': 'time'})
        return form

    def get_context_data(self, **kwargs):
        context = super(CreateEvent, self).get_context_data(**kwargs)
        context['button_text'] = 'Create Event'
        return context

    def dispatch(self, *args, **kwargs):
        return super(CreateEvent, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)

        cal_pk = self.kwargs.get('pk')
        cal = CalendarModel.objects.get(pk=cal_pk)

        obj.calendar = cal  
        obj.save() 

        member = Member.objects.get(user=self.request.user)

        part = Participants()
        part.member = member
        part.events = obj
        part.is_administrator = True
        part.save()

        success_url = "/calendar/" + str(cal_pk)
        return HttpResponseRedirect(success_url)

class UpdateEvent(UpdateView):
    template_name = 'create_edit_model.html'
    model = Event
    fields = ('name', 'description', 'date', 'time', 'end_time', 'public', 'sub_calendar', 'is_open')
    success_url = "/"

    def get_form(self):
        today = datetime.today()
        form = super(UpdateEvent, self).get_form()
        form.fields['date'].widget = SelectDateWidget()
        form.fields['time'].widget = TimeInput(attrs={'type': 'time'})
        form.fields['end_time'].widget = TimeInput(attrs={'type': 'time'})
        return form

    def get_context_data(self, **kwargs):
        context = super(UpdateEvent, self).get_context_data(**kwargs)
        context['button_text'] = 'Update Event'
        return context

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
        invitations = Invitation.objects.filter(events=eve)
        participants = Participants.objects.filter(events=eve)
        member = Member.objects.get(user=request.user)

        context = {
            'event': eve,
            'invitations': invitations,
            'participants': participants
        }

        try:
            my_participation = Participants.objects.get(events=eve, member=member)
            context.update({
                'my_part': True,
                'admin': my_participation.is_administrator
            })
            return render(request, self.template_name, context)
        except Participants.DoesNotExist:
            context.update({
                'my_part': False
            })
            return render(request, self.template_name, context)
            
        

        

class CreateFilter(CreateView):
    template_name = 'create_edit_model.html'
    model = Filter
    fields = ('name',)

    def get_context_data(self, **kwargs):
        context = super(CreateFilter, self).get_context_data(**kwargs)
        context['button_text'] = 'Create Sub Calendar'
        return context

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
