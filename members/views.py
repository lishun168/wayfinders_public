from django.shortcuts import render
from django.db.models import Q
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin
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
        member = MemberModel.objects.filter(pk=pk)
        memberskills = MemberSkills.objects.filter(member=pk)
        membercompanies = MemberCompany.objects.filter(member=pk)
        skills = Skill.objects.all()
        permissions = Permissions.objects.all()

        context = {
            'member': member,
            'member_skills': memberskills,
            'member_companies': membercompanies,
            'skills': skills,
            'permissions': permissions
        }
        logger.error(context)
        return render(request, self.template_name, context)

class MembersDirectory(View):
    template_name = 'members/members_directory.html'

    def get(self, request):
        members = MemberModel.objects.all()
        context = {
            'members': members
        }
        logger.error(context)
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
