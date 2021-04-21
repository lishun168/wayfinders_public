"""wayfinders URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from . import settings
from django.urls import path, include
from members.views import Index, Member, Company, MembersDirectory, DirectorySearch, LoginPage
from members.views import MyProfile, EditMember, CreateGroup, EditGroup, LeaveGroup
from members.views import MyGroups, MySkills, Invites, SignUp, CreateProfile, CreateSkill, ViewSkill
from members import views as member_views
from events import views as event_views
from forum import views as forums_views
from forum.views import ForumDirectory, ThreadPage, CreateDiscussion, UpdateDiscussion, CreatePost, UpdatePost, CreateReply, UpdateReply
from cal.views import Calendar, CreateEvent, UpdateEvent, ViewEvent, CreateFilter, CalendarDate
from events.views import CreateInvitation, Invite
from cal import views as calendar_views
from groups.views import GroupDirectory

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view()),
    path('profile/<int:pk>/', Member.as_view()),
    path('company/<int:pk>/', Company.as_view()),
    path('members/', MembersDirectory.as_view()),
    path('login_page', LoginPage.as_view()),
    path('login/', member_views.login_view),
    path('logout/', member_views.logout_view),
    path('search/<str:query>', DirectorySearch.as_view()),
    path('my_profile/', MyProfile.as_view()),
    path('edit_profile/<int:pk>', EditMember.as_view()),
    path('create_profile/', CreateProfile.as_view()),
    path('signup', SignUp.as_view()),
    path('forum', ForumDirectory.as_view()),
    path('forum/<int:pk>', ThreadPage.as_view()),
    path('forum/create', CreateDiscussion.as_view()),
    path('forum/update/<int:pk>', UpdateDiscussion.as_view()),
    path('forum/post/<int:pk>', CreatePost.as_view()),
    path('forum/post/update/<int:pk>', UpdatePost.as_view()),
    path('forum/reply/<int:pk>/<int:post_pk>', CreateReply.as_view()),
    path('forum/reply/update/<int:pk>', UpdateReply.as_view()),
    path('like/<int:member_pk>/<int:post_pk>', forums_views.like, name='like'),
    path('flag/<int:member_pk>/<int:post_pk>', forums_views.flag, name='flag'),
    path('calendar/<int:pk>', Calendar.as_view()),
    path('calendar/<int:pk>/<int:year>/<int:month>', CalendarDate.as_view()),
    path('edit_event/<int:pk>', UpdateEvent.as_view()),
    path('create_event/<int:pk>', CreateEvent.as_view()),
    path('event/<int:pk>', ViewEvent.as_view()),
    path('invite/<int:pk>', CreateInvitation.as_view()), #invite/{{event.pk}} - invite/1
    path('create_filter/<int:pk>', CreateFilter.as_view()),
    path('groups/', GroupDirectory.as_view()),
    path('group/<int:pk>', Company.as_view()),
    path('create_group/<int:pk>', CreateGroup.as_view()),
    path('create_skill/<int:pk>', CreateSkill.as_view()),
    path('edit_group/<int:pk>', EditGroup.as_view()),
    path('my_groups/<int:pk>', MyGroups.as_view()),
    path('my_skills/<int:pk>', MySkills.as_view()),
    path('invites/<int:pk>', Invites.as_view()),
    path('get_invite/<int:pk>', Invite.as_view()),
    path('leave_group/<int:pk>', LeaveGroup.as_view()),
    path('skill/<int:pk>', ViewSkill.as_view()),
    path('accept_invite/<int:invite_pk>', event_views.accept_view),
    path('decline_invite/<int:invite_pk>', event_views.decline_view),
    path('join_event/<int:event_pk>/<int:user_pk>', event_views.join_view),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
