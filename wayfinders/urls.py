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
from django.urls import path
from members.views import Index, Member, Company, MembersDirectory, DirectorySearch, LoginPage, MyProfile, EditMember, CreateMember
from members import views as member_views
from forum.views import ForumDirectory, ThreadPage

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
    path('forum/<int:pk>', ThreadPage.as_view())

]

urlpatterns += staticfiles_urlpatterns()
