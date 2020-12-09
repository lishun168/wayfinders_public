from django.db import models
from datetime import datetime
from members.models import Member


class Thread(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True, auto_now=False)
    created_by = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True)
    created_by_string = models.CharField(max_length=255)


    def __str__(self):
        return '%s' % (self.title)

class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    body = models.TextField()
    created_by = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True)
    created_by_string = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True, auto_now=False)
    edited_at = models.DateField(auto_now_add=True, auto_now=False)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' % (self.thread, self.created_at )

