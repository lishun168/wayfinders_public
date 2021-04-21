from django.views.generic.edit import CreateView, UpdateView
from .models import Invitation, Event, Participants
from members.models import Member
from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import render

class CreateInvitation(CreateView):
    template_name = 'create_edit_model.html'
    model = Invitation
    fields = ('member',)

    def get_context_data(self, **kwargs):
        context = super(CreateInvitation, self).get_context_data(**kwargs)
        context['button_text'] = 'Create Invitation'
        return context

    def dispatch(self, *args, **kwargs):
        return super(CreateInvitation, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        event_pk = self.kwargs.get('pk')
        event = Event.objects.get(pk=event_pk)
        obj.events = event
        obj.save()

        member_pk = self.kwargs.get('pk')
        success_url = '/profile/' + str(member_pk)
        return HttpResponseRedirect(success_url)

class Invite(View):
    template_name = 'events/invite.html'
    
    def get(self, request, pk):
        invite = Invitation.objects.get(pk=pk)
        event = Event.objects.get(pk=invite.events.pk)
        participants = Participants.objects.filter(events=event)
        invitations = Invitation.objects.filter(events=event)

        context = {
            'invite': invite,
            'event': event,
            'participants': participants,
            'invitations': invitations
        }

        return render(request, self.template_name, context)

def accept_view(request, invite_pk):
    invite = Invitation.objects.get(pk=invite_pk)
    invite.accept = True
    invite.decline = False
    invite.save()

    participant = Participants()
    participant.events = invite.events
    participant.member = invite.member
    participant.save()

    success_url = '/profile/' + str(invite.member.pk)
    return HttpResponseRedirect(success_url)
    

def decline_view(request, invite_pk):
    invite = Invitation.objects.get(pk=invite_pk)
    invite.decline = True
    invite.accept = False
    invite.save()

    try:
        participant = Participants.objects.get(events=invite.events, member=invite.member)
        participant.delete()
    except Participants.DoesNotExist:
        empty_var = 1

    success_url = '/profile/' + str(invite.member.pk)
    return HttpResponseRedirect(success_url)

def join_view(request, event_pk, user_pk):
    member = Member.objects.get(user=user_pk)
    event = Event.objects.get(event=event_pk)

    participant = Participant()
    participant.member = member
    participant.events = event
    participant.save()

    success_url = '/event/' + str(event_pk)
    return HttpResponseRedirect(success_url)



# Create your views here.
