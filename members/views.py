from django.shortcuts import render, redirect
from django.db.models import Q
from django.views import View
from . import forms as my_forms
from django.urls import reverse
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from .models import Member as MemberModel
from .models import Company as CompanyModel
from .models import Role, Permissions, Skill, Industry, Gallery, MemberSkills, MemberCompany

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
        member = MemberModel.objects.filter(user=request.user.pk)
        id = 1
        for m in member:
            logger.error(m.pk)
            id = m.pk
        
        address = '/profile/' + str(id)
        return HttpResponseRedirect(address)

class Member(View):
    template_name = 'members/profile.html'

    def get(self, request, pk):
        my_profile = False
        member = MemberModel.objects.get(pk=pk)
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
            'my_profile': my_profile
        }
        return render(request, self.template_name, context)

class EditMember(UpdateView):
    template_name = 'members/edit_profile.html'
    model = MemberModel
    fields = '__all__'
    success_url = "/"
    
class CreateMember(CreateView):
    template_name = 'members/create_profile.html'
    model = MemberModel
    fields = '__all__'
    success_url = "/"

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

class Company(View):
    template_name = 'members/company.html'

    def get(self, request, pk):
        company = Company.objects.filter(pk=pk)
        context = {
            'company': company
        }
        return render(request, self.template_name, context)


def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")

def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("/")

    if request.method == 'GET':
        form = UserCreationForm()
        return(request, 'signup.html', {'form': form})
    return(request, 'signup.html', {'form': form})


