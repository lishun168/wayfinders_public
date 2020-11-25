from django import forms
from .models import Member 

class EditMemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'

    def edit_profile(self):
        pass