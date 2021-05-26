from django.shortcuts import render
from django.db.models import Q
from django.views import View
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.contrib.auth.models import User
from login.views import LoginPermissionMixin
from login.views import WFAdminPermissionMixin
from django.core.exceptions import PermissionDenied 
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from .forms import ApplicationForm

##           MODELS             ##
from .models import MemberUser
from .models import Member
from .models import UserRole
from .models import Permissions
from .models import Application as ApplicationModel
from skills.models import Skill
from skills.models import MemberToSkills
from cal.models import Calendar
from events.models import Invitation
from events.models import Participants
from industries.models import MemberToIndustry
##                              ##

import logging
logger = logging.getLogger(__name__)

class Index(View):
    template_name = 'members/index.html'

    def get(self, request):
        return render(request, self.template_name)

class MyProfile(LoginPermissionMixin, View):
    def get(self, request):
        member = MemberUser.objects.get(user=request.user.pk)
        id = member.pk
        
        address = '/profile/' + str(id)
        return HttpResponseRedirect(address)

class UserProfile(LoginPermissionMixin, View):
    template_name = 'members/profile.html'

    def get(self, request, pk):
        my_profile = False
        user = MemberUser.objects.get(pk=pk)
        calendar = Calendar.objects.get(user=user)
        memberskills = MemberToSkills.objects.filter(member=pk)
        user_role = UserRole.objects.get(user=user)

        if request.user is not None:
            mId = request.user.pk
            user_member = MemberUser.objects.get(user=mId)
            if(user_member.pk == user.pk):
                my_profile = True

        context = {
            'profile': user,
            'member_skills': memberskills,
            'user_role': user_role,
            'my_profile': my_profile,
            'calendar': calendar
        }
        return render(request, self.template_name, context)

class EditUser(LoginPermissionMixin, UpdateView):
    template_name = 'create_edit_model.html'
    model = MemberUser
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
        'bio',
        'main_image'
        )

    def get_object(self, *args, **kwargs):
        obj = super(EditUser, self).get_object(*args, **kwargs)
        try:
            member = MemberUser.objects.get(user=self.request.user)
            if member.pk != self.kwargs.get('pk'):
                raise PermissionDenied()
        except MemberUser.DoesNotExist:
            raise PermissionDenied()
        return obj

    def get_context_data(self, **kwargs):
        context = super(EditUser, self).get_context_data(**kwargs)
        context['button_text'] = 'Edit Profile'
        return context

    def dispatch(self, *args, **kwargs):
        return super(EditUser, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()

        member_pk = self.kwargs.get('pk')

        success_url = '/profile/' + str(member_pk)
        return HttpResponseRedirect(success_url)

class CreateUser(CreateView):
    template_name = 'create_edit_model.html'
    model = MemberUser
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
        context = super(CreateUser, self).get_context_data(**kwargs)
        context['button_text'] = 'Create Profile'
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        user = User.objects.get(pk=self.request.user.pk)
        obj.user = user
        obj.membership_since = timezone.now()
        obj.save() 
        
        calendar = Calendar()
        calendar.public = True
        calendar.name = "Calendar for " + obj.first_name + " " + obj.last_name
        calendar.member = obj

        calendar.save()

        success_url = "/pending_approval"
        return HttpResponseRedirect(success_url)

class CreateMemberProfile(CreateView):
    template_name = 'create_edit_model.html'
    model = MemberUser
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
        context = super(CreateMemberProfile, self).get_context_data(**kwargs)
        context['button_text'] = 'Create Profile'
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        user = User.objects.get(pk=self.request.user.pk)
        obj.user = user
        obj.membership_since = timezone.now()
        obj.save() 
        
        calendar = Calendar()
        calendar.public = True
        calendar.name = "Calendar for " + obj.first_name + " " + obj.last_name
        calendar.member = obj

        calendar.save()

        success_url = "/pending_approval"
        return HttpResponseRedirect(success_url)

class MembersDirectory(View):
    template_name = 'members/members_directory.html'

    def get(self, request):
        members = Member.objects.all()
        context = {
            'members': members
        }
        
        return render(request, self.template_name, context)
        
class DirectorySearch(View):
    template_name='members/members_directory.html'

    def get(self, request, query):
        members = Member.objects.filter(Q(name__icontains=query))

        context = {
            'members': members,
            'query': query
        }

        return render(request, self.template_name, context)

class MemberView(View):
    template_name = 'members/member.html'

    def get(self, request, pk):
        member = Member.objects.get(pk=pk)
        member_skills = MemberToSkills.objects.filter(member=member)
        member_industries = MemberToIndustry.objects.filter(member=member)

        context = {
            'member': member,
            'member_skills': member_skills,
            'member_industries': member_industries
        }

        if request.user.is_authenticated == True:
            user_member = MemberUser.objects.get(user=request.user.pk)
            context['wf_admin'] = user_member.is_wf_admin
            if user_member.member == member:
                user_role = UserRole.objects.get(user=user_member)
                context['member_admin'] = user_role.permissions.is_member_admin
                context['member_of'] = True
            else:
                context['member_admin'] = False
                context['member_of'] = False

        return render(request, self.template_name, context)

class Invites(LoginPermissionMixin, View):
    template_name = 'members/invites.html'

    def get_object(self, *args, **kwargs):
        obj = super(Invites, self).get_object(*args, **kwargs)
        try:
            member = MemberUser.objects.get(user=self.request.user)
            if member.pk != self.kwargs.get('pk'):
                raise PermissionDenied()
        except MemberUser.DoesNotExist:
            raise PermissionDenied()
        return obj

    def get(self, request, pk):
        member = MemberUser.objects.get(pk=pk)

        # PERMISSIONS #
        my_member = MemberUser.objects.get(user=request.user)

        if member != my_member:
            raise PermissionDenied()

        invites = Invitation.objects.filter(member=member)
        participations = Participants.objects.filter(member=member)

        context = {
            'invites': invites,
            'profile': member,
            'participations': participations
        }

        return render(request, self.template_name, context)

class SignUpForm(WFAdminPermissionMixin, UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)


class SignUp(WFAdminPermissionMixin, CreateView):
    template_name = 'members/signup.html'
    form_class = SignUpForm

    def get_object(self, *args, **kwargs):
        obj = super(SignUp, self).get_object(*args, **kwargs)
        try:
            member_pk = self.kwargs.get('pk')
            member_user = MemberUser.objects.get(user=self.request.user)
            member = Member.objects.get(pk=member_pk)
            if member != member_user.member:
                raise PermissionDenied()
        except Member.DoesNotExist:
            raise PermissionDenied()
        return obj

    def get_context_data(self, **kwargs):
        context = super(SignUp, self).get_context_data(**kwargs)
        context['button_text'] = 'Create Member'
        return context

    def dispatch(self, *args, **kwargs):
        return super(SignUp, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        

        member_pk = self.kwargs.get('pk')
        member = Member.objects.get(pk=member_pk)

        obj.member = member
        obj.save()

        success_url = '/signup/' + str(member_pk)
        return HttpResponseRedirect(success_url)

class Approval(View):
    template_name = 'members/pending_approval.html'

    def get(self, request):
        return render(request, self.template_name, {})

class UpdatePassword(PasswordChangeView):
    template_name = 'members/controls/update_password.html'
    success_url = '/my_profile'
    form_class = PasswordChangeForm

class Application(View):
    template_name = 'members/application.html'
    form_class = ApplicationForm

    def get(self, request, *args, **kwargs):
        form = ApplicationForm
        context = {
            'form': form
        }
        
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            organization_name = form.cleaned_data['organization_name']
            organization_email = form.cleaned_data['organization_email']

            application = ApplicationModel()
            application.name = name
            application.email = email
            application.org_name = organization_name
            application.org_email = organization_email
            application.save()

            return HttpResponseRedirect('/submission')


class ApplicationSubmission(View):
    template_name = "members/application_submission.html"
    
    def get(self, request):
        return render(request, self.template_name, {})



