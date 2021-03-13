from django.views.generic.edit import CreateView, UpdateView
from .models import Invitation, Event
from django.http import HttpResponseRedirect

class CreateInvitation(CreateView):
    template_name = 'events/create_invitation.html'
    model = Invitation
    fields = ('member',)

    def dispatch(self, *args, **kwargs):
        return super(CreateInvitation, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        event_pk = self.kwargs.get('pk')
        event = Event.objects.get(pk=event_pk)
        obj.events = event
        obj.save()      

        success_url = '/'
        return HttpResponseRedirect(success_url)



# Create your views here.
