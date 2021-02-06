from django.contrib import admin

from .models import Company, Member, Skill, Role, Permissions, Industry, Gallery, MemberCompany, MemberSkills, CompanyIndustry
from cal.models import Calendar as CalendarModel

# Member Inlines #
class MemberCompanyAdmin(admin.TabularInline):
    model = MemberCompany

class MemberSkillsAdmin(admin.TabularInline):
    model = MemberSkills

class CalendarInline(admin.TabularInline):
    model = CalendarModel

class MemberAdmin(admin.ModelAdmin):
    inlines = [MemberCompanyAdmin, MemberSkillsAdmin, CalendarInline]

# Company Inlines #
class CompanyIndustryAdmin(admin.TabularInline):
    model = CompanyIndustry

class CompanyAdmin(admin.ModelAdmin):
    inlines = [CompanyIndustryAdmin, CalendarInline]

# Register Admins #
admin.site.register(Company, CompanyAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Skill)
admin.site.register(Role)
admin.site.register(Permissions)
admin.site.register(Industry)
admin.site.register(Gallery)


