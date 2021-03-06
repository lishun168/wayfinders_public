from django.shortcuts import render
from django.views import View
from .models import Groups

class GroupDirector(View):
    template_name="groups/groups_index.html"

    def get(self, request):
        groups = Groups.objects.all()

        context = {
            'groups': groups
        }

        return render(request, self.template_name, context)