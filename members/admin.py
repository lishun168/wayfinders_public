from django.contrib import admin

from .models import Application, Member
from .models import MemberUser
from .models import UserRole
from .models import Permissions
from .models import Gallery
from skills.models import MemberToSkills
from skills.models import UserToSkills
from cal.models import Calendar
from industries.models import MemberToIndustry

#class UserToMemberAdmin(admin.TabularInline):
#    model = MemberUser

class UserRoleInline(admin.TabularInline):
    model = UserRole

class UserToSkillsAdmin(admin.TabularInline):
    model = UserToSkills

class CalendarInline(admin.TabularInline):
    model = Calendar

class UserAdmin(admin.ModelAdmin):
    inlines = [UserRoleInline, UserToSkillsAdmin, CalendarInline]

class MemberToIndustryAdmin(admin.TabularInline):
    model = MemberToIndustry

class MemberToSkillsAdmin(admin.TabularInline):
    model = MemberToSkills

class MemberAdmin(admin.ModelAdmin):
    inlines = [MemberToIndustryAdmin, MemberToSkillsAdmin, CalendarInline]

class UserRoleInline(admin.TabularInline):
    model = UserRole

class PermissionsAdmin(admin.ModelAdmin):
    inlines = [UserRoleInline]

# Register Admins #
admin.site.register(Member, MemberAdmin)
admin.site.register(MemberUser, UserAdmin)
admin.site.register(UserRole)
admin.site.register(Permissions, PermissionsAdmin)
admin.site.register(Gallery)
admin.site.register(Application)


