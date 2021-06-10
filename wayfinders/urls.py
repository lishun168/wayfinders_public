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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.urls import static
from . import settings
from django.urls import path, include
from login.views import LoginPage
from login import views as login_views
from events import views as event_views
from forum import views as forums_views
from members.views import CreateMemberProfile, UpdatePassword
from members.views import Index
from members.views import UserProfile 
from members.views import MemberView
from members.views import EditMember
from members.views import EditMembersList
from members.views import MembersDirectory
from members.views import DirectorySearch
from members.views import MyProfile
from members.views import EditUser
from members.views import PermissionsView
from members.views import CreatePermissions
from members.views import EditPermissions
from members.views import Roles
from members.views import AssignRoles
from members.views import UpdateRoles
from members.views import RolesEditAll
from members.views import Invites
from members.views import SignUp
from members.views import CreateUser
from members.views import Approval
from members.views import UpdatePassword
from members.views import Application
from members.views import ApplicationSubmission
from skills.views import CreateSkill
from skills.views import ViewSkill
from skills.views import MySkills
from groups.views import CreateGroup
from groups.views import EditGroup
from groups.views import LeaveGroup
from groups.views import MyGroups
from forum.views import ForumDirectory
from forum.views import ThreadPage
from forum.views import CreateDiscussion
from forum.views import UpdateDiscussion
from forum.views import CreatePost
from forum.views import UpdatePost
from forum.views import CreateReply
from forum.views import UpdateReply
from cal.views import Calendar
from cal.views import CreateFilter
from cal.views import CalendarDate
from events.views import CreateInvitation
from events.views import Invite
from events.views import CreateEvent
from events.views import UpdateEvent
from events.views import ViewEvent
from events.views import CreateBooking
from events.views import BookEvent
from events.views import MarkBusy
from search.views import Search

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view()),

    ## MEMBERS APP ##
    path('profile/<int:pk>/', UserProfile.as_view()),
    path('my_profile/', MyProfile.as_view()),
    path('edit_profile/<int:pk>', EditUser.as_view()),
    path('create_member/', CreateUser.as_view()),
    path('change_password/', UpdatePassword.as_view()),
    
    path('members/', MembersDirectory.as_view()),
    path('member/<int:pk>', MemberView.as_view()),
    path('pending_approval', Approval.as_view()),
    path('create_profile/', CreateMemberProfile.as_view()),
    path('edit_member/<int:pk>', EditMember.as_view()),
    path('edit_member_list/<int:pk>', EditMembersList.as_view()),

    path('permissions/<int:pk>', PermissionsView.as_view()),
    path('create_permissions/<int:member_pk>/', CreatePermissions.as_view()),
    path('edit_permissions/<int:pk>/<int:member_pk>/', EditPermissions.as_view()),

    path('roles/<int:pk>', Roles.as_view()),
    path('create_role/<int:member_pk>', AssignRoles.as_view()),
    path('edit_role/<int:pk>/<int:member_pk>/', UpdateRoles.as_view()),
    path('edit_all_roles/<int:pk>/', RolesEditAll.as_view()),
    #Update Many    

    path('application/', Application.as_view()),
    path('submission/', ApplicationSubmission.as_view()),

    ## LOGIN APP ##
    path('login_page', LoginPage.as_view()),
    path('login/', login_views.login_view),
    path('logout/', login_views.logout_view),
    path('signup/<int:pk>', SignUp.as_view()),

    ## FORUM APP ##
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
    path('sticky/<int:discussion_pk>', forums_views.sticky),

    ## CALENDAR APP ##
    path('calendar/<int:pk>', Calendar.as_view()),
    path('calendar/<int:pk>/<int:year>/<int:month>', CalendarDate.as_view()),
    path('create_filter/<int:pk>', CreateFilter.as_view()),

    ## EVENT APP ##
    path('edit_event/<int:pk>', UpdateEvent.as_view()),
    path('create_event/<int:pk>', CreateEvent.as_view()),
    path('create_booking/<int:pk>', CreateBooking.as_view()),
    path('mark_busy/<int:pk>', MarkBusy.as_view()),
    path('book_event/<int:pk>/<int:cal_pk>', BookEvent.as_view()),
    path('event/<int:pk>', ViewEvent.as_view()),
    path('invite/<int:pk>', CreateInvitation.as_view()), 
    path('accept_invite/<int:invite_pk>', event_views.accept_view),
    path('decline_invite/<int:invite_pk>', event_views.decline_view),
    path('join_event/<int:event_pk>/<int:user_pk>', event_views.join_view),
    path('invites/<int:pk>', Invites.as_view()),
    path('get_invite/<int:pk>', Invite.as_view()),
    
    ## GROUP APP 
    path('create_group/<int:pk>', CreateGroup.as_view()),
    path('edit_group/<int:pk>', EditGroup.as_view()),
    path('my_groups/<int:pk>', MyGroups.as_view()),
    path('leave_group/<int:pk>', LeaveGroup.as_view()),

    ## SKILL APP ##
    path('create_skill/<int:pk>', CreateSkill.as_view()),
    path('my_skills/<int:pk>', MySkills.as_view()),
    path('skill/<int:pk>', ViewSkill.as_view()),

    ## SEARCH APP ##
    path('global_search/<str:query>', Search.as_view()),
    path('search/<str:query>', DirectorySearch.as_view()),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
