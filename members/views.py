from django.shortcuts import render, redirect
from django.forms.models import inlineformset_factory
from django.db.models import Q
from django.views import View
from . import forms as my_forms
from django.urls import reverse
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from .models import Member as MemberModel
from .models import Company as CompanyModel
from .models import Role as RoleModel
from .models import Permissions, Skill, Industry, Gallery, MemberSkills, MemberCompany
from cal.models import Calendar
from events.models import Invitation, Participants
from django.contrib.auth.models import User

import logging
logger = logging.getLogger(__name__)

class Index(View):
    template_name = 'members/index.html'

    def get(self, request):
        return render(request, self.template_name)

class LoginPage(SuccessMessageMixin, LoginView):
    template_name = 'members/login.html'
    success_url = '/login'
    success_message = 'Thank you for logging in'

class MyProfile(View):
    def get(self, request):
        member = MemberModel.objects.get(user=request.user.pk)
        id = member.pk
        
        address = '/profile/' + str(id)
        return HttpResponseRedirect(address)

class Member(View):
    template_name = 'members/profile.html'

    def get(self, request, pk):
        my_profile = False
        member = MemberModel.objects.get(pk=pk)
        calendar = Calendar.objects.get(member=member)
        memberskills = MemberSkills.objects.filter(member=pk)
        membercompanies = MemberCompany.objects.filter(member=pk)
        skills = Skill.objects.all()
        permissions = Permissions.objects.all()

        if request.user is not None:
            mId = request.user.pk
            user_member = MemberModel.objects.get(user=mId)
            if(user_member.pk == member.pk):
                my_profile = True

        context = {
            'profile': member,
            'member_skills': memberskills,
            'member_companies': membercompanies,
            'skills': skills,
            'permissions': permissions,
            'my_profile': my_profile,
            'calendar': calendar
        }
        return render(request, self.template_name, context)

class EditMember(UpdateView):
    template_name = 'create_edit_model.html'
    model = MemberModel
    fields = fields = (
        'first_name', 
        'last_name', 
        'job_title', 
        'address', 
        'address_2', 
        'city',
        'province',
        'country',
        'postal_code',
        'business_phone',
        'home_phone',
        'cell_phone',
        'email',
        'website',
        'bio',
        'publicly_viewable',
        'main_image'
        )

    def get_context_data(self, **kwargs):
        context = super(EditMember, self).get_context_data(**kwargs)
        context['button_text'] = 'Edit Profile'
        return context

    def dispatch(self, *args, **kwargs):
        return super(EditMember, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()

        member_pk = self.kwargs.get('pk')

        success_url = '/profile/' + str(member_pk)
        return HttpResponseRedirect(success_url)

    

class CreateProfile(CreateView):
    template_name = 'create_edit_model.html'
    model = MemberModel
    fields = (
        'first_name', 
        'last_name', 
        'job_title', 
        'address', 
        'address_2', 
        'city',
        'province',
        'country',
        'postal_code',
        'business_phone',
        'email',
        'website',
        'bio',
        'publicly_viewable',
        'main_image'
        )

    def get_context_data(self, **kwargs):
        context = super(CreateProfile, self).get_context_data(**kwargs)
        context['button_text'] = 'Create Profile'
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        user = User.objects.get(pk=self.request.user.pk)
        obj.user = user
        obj.save() 
        
        calendar = Calendar()
        calendar.public = True
        calendar.name = "Calendar for " + obj.first_name + " " + obj.last_name
        calendar.member = obj

        calendar.save()

        success_url = "/"
        return HttpResponseRedirect(success_url)
    

class MembersDirectory(View):
    template_name = 'members/members_directory.html'

    def get(self, request):
        members = MemberModel.objects.all()
        context = {
            'members': members
        }
        
        return render(request, self.template_name, context)
        

class DirectorySearch(View):
    template_name='members/members_directory.html'

    def get(self, request, query):
        members = MemberModel.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(job_title__icontains=query))

        context = {
            'members': members
        }

        return render(request, self.template_name, context)

class MyGroups(View):
    template_name = 'members/my_groups.html'

    def get(self, request, pk):
        member = MemberModel.objects.get(pk=pk)
        member_groups = MemberCompany.objects.filter(member=member)

        context = {
            'member_groups': member_groups,
            'profile': member
        }

        return render(request, self.template_name, context)

class MySkills(View):
    template_name = 'members/my_skills.html'

    def get(self, request, pk):
        member = MemberModel.objects.get(pk=pk)
        member_skills = MemberSkills.objects.filter(member=member)

        context = {
            'member_skills': member_skills,
            'profile': member
        }

        return render(request, self.template_name, context)

class Company(View):
    template_name = 'members/company.html'

    def get(self, request, pk):
        company = CompanyModel.objects.get(pk=pk)
        company_admin = False
        is_member = False

        if request.user.is_authenticated == False:
            return render(request, self.template_name, {'company': company})
        else:
            user_member = MemberModel.objects.get(user=request.user.pk)
            try:
                member_company = MemberCompany.objects.get(member=user_member, company=company)
            except MemberCompany.DoesNotExist:
                return render(request, self.template_name, {'company': company})

            

        context = {
            'company': company,
            'member_company': member_company,
            'company_admin': member_company.role.can_edit_company_profile,
            'company_member': True
        }
        return render(request, self.template_name, context)

class EditGroup(UpdateView):
    template_name = 'create_edit_model.html'
    model = CompanyModel
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(EditGroup, self).get_context_data(**kwargs)
        context['button_text'] = 'Edit Group'
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save() 

        pk=obj.pk

        success_url = "/group/" + str(pk)
        return HttpResponseRedirect(success_url)

class LeaveGroup(DeleteView):
    template_name = 'create_edit_model.html'
    model = MemberCompany
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(LeaveGroup, self).get_context_data(**kwargs)
        context['button_text'] = 'Confirm to Leave the Group'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        member = MemberModel.objects.get(user=request.user)
        success_url = "/profile/" + str(member.pk)
        return HttpResponseRedirect(success_url)

    
class CreateGroup(CreateView):
    template_name = 'create_edit_model.html'
    model = CompanyModel
    fields = '__all__'

    def dispatch(self, *args, **kwargs):
        return super(CreateGroup, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateGroup, self).get_context_data(**kwargs)
        context['button_text'] = 'Create Group'
        return context

    def form_valid(self, form):
        logger.error("form_valid")
        obj = form.save(commit=False)
        member_pk = self.kwargs.get('pk')
        member = MemberModel.objects.get(pk=member_pk)
        obj.save() 
        role = RoleModel()
        role.title = obj.name + " admin"
        role.can_create_forum_group = True
        role.can_post_to_forums = True
        role.can_add_calendar_events = True
        role.can_see_all_members = True
        role.can_edit_company_profile = True
        role.can_see_company_console = True
        role.can_add_employees = True
        role.can_delete_posts = True
        role.is_account_manager = True
        role.is_calendar_manager = True
        role.save()

        calendar = Calendar()
        calendar.public = True
        calendar.name = "Calendar for " + obj.name 
        calendar.company = obj

        member_company = MemberCompany()
        member_company.role = role
        member_company.member = member
        member_company.company = obj
        member_company.save()
        
       

        group_pk = obj.pk
        logger.error(obj.pk)

        success_url = "/group/" + str(group_pk)
        return HttpResponseRedirect(success_url)


class CreateSkill(CreateView):
    template_name = 'create_edit_model.html'
    model = Skill
    fields = ('name', 'description')

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
        member = MemberModel.objects.get(pk=member_pk)
        member_skill = MemberSkills()
        member_skill.skill = obj
        member_skill.member = member
        member_skill.save()

        success_url = "/profile/" + str(member_pk)
        return HttpResponseRedirect(success_url)

class ViewSkill(View):
    template_name = 'members/skill.html'

    def get(self, request, pk):
        skill = Skill.objects.get(pk=pk)
        context = {
            'skill': skill
        }

        return render(request, self.template_name, context)


class Invites(View):
    template_name = 'members/invites.html'

    def get(self, request, pk):
        member = MemberModel.objects.get(pk=pk)
        invites = Invitation.objects.filter(member=member)
        participations = Participants.objects.filter(member=member)

        context = {
            'invites': invites,
            'profile': member,
            'participations': participations
        }

        return render(request, self.template_name, context)

class SignUpForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

class SignUp(CreateView):
    template_name = 'members/signup.html'
    success_url = '/create_profile'
    form_class = SignUpForm

def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        try:
            member = MemberModel.objects.get(user=user)
            return HttpResponseRedirect("/")
        except MemberModel.DoesNotExist:
            return HttpResponseRedirect("/create_profile")
    else:
        message = 'The username or password is incorrect'
        return render(request, 'members/login_failed.html', {'message': message})

        #TODO
        #LOGIN FAILED

def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


