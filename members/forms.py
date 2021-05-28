from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ApplicationForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=255)
    email = forms.EmailField(label='Your Email', max_length=255)
    organization_name = forms.CharField(label='Organization Name', max_length=255)
    organization_email = forms.EmailField(label='Organization Email', max_length=255)

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='New User Name', max_length=255)
    last_name = forms.CharField(label='New User Last Name', max_length=255)
    email = forms.EmailField(label="New User Email", max_length=255)
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)


