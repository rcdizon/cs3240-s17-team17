from django import forms
from .models import Report
from .models import Message


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email:", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    widgets = {
        'password' : forms.PasswordInput(),
    }

class CreateReport(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('companyName', 'companyLocation', 'companyPhone', 'companyCountry', 'currentProjects', 'industry', 'sector')

class SendMessage(forms.ModelForm):
	class Meta:
		model = Message
		fields = ('reciever','textbox')