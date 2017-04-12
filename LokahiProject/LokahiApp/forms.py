from django import forms
from .models import Report


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email:", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    widgets = {
        'password' : forms.PasswordInput(),
    }


class CreateReport(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('companyName', 'companyLocation', 'companyPhone', 'companyCountry',
                  'currentProjects', 'industry', 'sector', 'upload', 'encrypted')
