from django import forms

class ApplicationForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=255)
    email = forms.EmailField(label='Your Email', max_length=255)
    organization_name = forms.CharField(label='Organization Name', max_length=255)
    organization_email = forms.EmailField(label='Organization Email', max_length=255)


