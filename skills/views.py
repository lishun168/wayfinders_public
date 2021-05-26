from django.shortcuts import render
from login.views import LoginPermissionMixin
from django.core.exceptions import PermissionDenied 
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.edit import UpdateView, CreateView
from members.models import MemberUser
from .models import MemberToSkills, UserToSkills, Skill

# Create your views here.

class CreateSkill(LoginPermissionMixin, CreateView):
    template_name = 'create_edit_model.html'
    model = Skill
    fields = ('name', 'description')

    def get_object(self, *args, **kwargs):
        obj = super(CreateSkill, self).get_object(*args, **kwargs)
        try:
            member = MemberUser.objects.get(user=self.request.user)
            if member.pk != self.kwargs.get('pk'):
                raise PermissionDenied()
        except MemberUser.DoesNotExist:
            raise PermissionDenied()
        return obj

    def dispatch(self, *args, **kwargs):
        return super(CreateSkill, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateSkill, self).get_context_data(**kwargs)
        context['button_text'] = 'Create Skill'
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save() 

        member_pk = self.kwargs.get('pk')
        member = MemberUser.objects.get(pk=member_pk)
        member_skill = UserToSkills()
        member_skill.skill = obj
        member_skill.member = member
        member_skill.save()

        success_url = "/profile/" + str(member_pk)
        return HttpResponseRedirect(success_url)

class ViewSkill(LoginPermissionMixin, View):
    template_name = 'members/skill.html'

    def get(self, request, pk):
        skill = Skill.objects.get(pk=pk)
        context = {
            'skill': skill
        }

        return render(request, self.template_name, context)

class MySkills(LoginPermissionMixin, View):
    template_name = 'members/my_skills.html'

    def get(self, request, pk):
        member = MemberUser.objects.get(pk=pk)
        member_skills = MemberToSkills.objects.filter(member=member)

        context = {
            'member_skills': member_skills,
            'profile': member
        }

        return render(request, self.template_name, context)