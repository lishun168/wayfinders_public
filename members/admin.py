from django.contrib import admin

from .models import Company, Member, Skill, Role, Permissions, Industry, Gallery, MemberCompany, MemberSkills, CompanyIndustry


# Member Inlines #
class MemberCompanyAdmin(admin.TabularInline):
    model = MemberCompany

class MemberSkillsAdmin(admin.TabularInline):
    model = MemberSkills

class MemberAdmin(admin.ModelAdmin):
    inlines = [MemberCompanyAdmin, MemberSkillsAdmin]

# Company Inlines #
class CompanyIndustryAdmin(admin.TabularInline):
    model = CompanyIndustry

class CompanyAdmin(admin.ModelAdmin):
    inlines = [CompanyIndustryAdmin]

# Register Admins #
admin.site.register(Company, CompanyAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Skill)
admin.site.register(Role)
admin.site.register(Permissions)
admin.site.register(Industry)
admin.site.register(Gallery)


