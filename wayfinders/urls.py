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
from django.urls import path, include
from members.views import Index, Member, Company, MembersDirectory, DirectorySearch, LoginPage, MyProfile, EditMember, CreateMember
from members import views as member_views
from forum import views as forums_views
from forum.views import ForumDirectory, ThreadPage, CreateDiscussion, CreatePost
from cal.views import Calendar, CreateEvent, UpdateEvent, ViewEvent, CreateFilter
from cal import views as calendar_views

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
    path('create_profile/', CreateMember.as_view()),
    path('signup', member_views.signup, name='signup'),
    path('forum', ForumDirectory.as_view()),
    path('forum/<int:pk>', ThreadPage.as_view()),
    path('forum/create', CreateDiscussion.as_view()),
    path('forum/post/<int:pk>', CreatePost.as_view()),
    path('like', forums_views.like, name='like'),
    path('flag', forums_views.flag, name='flag'),
    path('calendar/<int:pk>', Calendar.as_view()),
    path('edit_event/<int:pk>', UpdateEvent.as_view()),
    path('create_event/<int:pk>', CreateEvent.as_view()),
    path('event/<int:pk>', ViewEvent.as_view()),
    path('create_filter/<int:pk>', CreateFilter.as_view()),

]

urlpatterns += staticfiles_urlpatterns()
