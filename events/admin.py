from django.contrib import admin
from .models import Event, Invitation, Participants
# Register your models here.

admin.site.register(Event)
admin.site.register(Invitation)
admin.site.register(Participants)
