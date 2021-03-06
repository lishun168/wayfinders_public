from django.views.generic.edit import CreateView, UpdateView
from .models import Invitation
from django.http import HttpResponseRedirect

class CreateInvitation(CreateView):
    template_name = 'create_invitation.html'
    model = Invitation
    fields = ('member','event')

    def dispatch(self, *args, **kwargs):
        return super(CreateInvitation, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)

        obj.save()

        success_url = '/'
        return HttpResponseRedirect(success_url)



# Create your views here.
