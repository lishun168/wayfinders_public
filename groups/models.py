from django.db import models
from members.models import Member

class Groups(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField()


    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name="Group"
        verbose_name_plural="Groups"

class Rules(models.Model):
    name=models.CharField(max_length=255)

class GroupToMember(models.Model):
    member=models.ForeignKey(Member, on_delete=models.CASCADE)
    group=models.ForeignKey(Groups, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.group, self.member)

#many to many reference to members