from django.db import models
from django.conf import settings
from datetime import datetime
from phonenumber_field.modelfields import PhoneNumberField

class Member(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    business_phone = PhoneNumberField()
    home_phone = PhoneNumberField(null=True, blank=True)
    cell_phone = PhoneNumberField(null=True, blank=True)
    email = models.EmailField(max_length=255)
    website = models.URLField(max_length=255)
    bio = models.TextField()
    publicly_viewable = models.BooleanField(u'Public', default=True)
    membership_expiry = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    membership_since = models.DateField(auto_now_add=False, blank=True, null=True)
    main_image = models.ImageField(upload_to="profile_gallery", blank=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    main_image = models.ImageField(upload_to="profile_gallery", blank=True)
    public = models.BooleanField(default=True)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name='Group'
        verbose_name_plural='Groups'

class Role(models.Model):
    title = models.CharField(max_length=255)
    can_create_forum_group = models.BooleanField(default=False)
    can_post_to_forums = models.BooleanField(default=False)
    can_add_calendar_events = models.BooleanField(default=False)
    can_see_all_members = models.BooleanField(default=False)
    can_edit_company_profile = models.BooleanField(default=False)
    can_see_company_console = models.BooleanField(default=False)
    can_add_employees = models.BooleanField(default=False)
    can_delete_posts = models.BooleanField(default=False)
    is_account_manager = models.BooleanField(default=False)
    is_calendar_manager = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.title)

class Permissions(models.Model):
    role_permissions = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.role_permissions + " Permissions")

    class Meta:
        verbose_name='Permission'
        verbose_name_plural='Permissions'

class Skill(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    official = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.name)

class Industry(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name='Industry'
        verbose_name_plural='Industries'

class Gallery(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='members/static/members/gallery/')

    def __str__(self):
        return '%s: %s' % (self.company, self.image)

    class Meta:
        verbose_name="Gallery"
        verbose_name_plural="Galleries"


class MemberCompany(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '%s: %s' % (self.company, self.member)

    class Meta:
        verbose_name="Member Companies"
        verbose_name_plural="Member Companies"

class MemberSkills(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    def __str__(self):
        return '%s: %s' % (self.member, self.skill)

    class Meta:
        verbose_name="Member Skills"
        verbose_name_plural="Member Skills"

class CompanyIndustry(models.Model):
    company = models.ForeignKey(Company, on_delete = models.CASCADE)
    industry = models.ForeignKey(Industry, on_delete = models.CASCADE)

    def __str__(self):
        return '%s: %s' % (self.company, self.industry)

    class Meta:
        verbose_name="Company Industry"
        verbose_name_plural="Company Industries"
    
