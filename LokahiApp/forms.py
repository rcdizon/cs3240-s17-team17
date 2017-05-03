from django import forms
from .models import Report
from .models import Upload
from .models import Message
from .models import Search
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group, Permission


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email:", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    widgets = {
        'password': forms.PasswordInput(),
    }


class CreateReport(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('companyName', 'companyCEO', 'companyLocation', 'companyPhone', 'companyCountry',
                  'currentProjects', 'industry', 'sector', 'privacy', 'keywords')


class CreateReportUpload(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ('fileupload', 'encrypted',)


class SendMessage(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('recipient','textbox',)


class RegisterForm(UserCreationForm):
    fullname = forms.CharField(label="Full name")
    CHOICES = (('Company User', 'Company User'), ('Investor', 'Investor'),)
    user_type = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = User
        fields = ("username", "fullname", "user_type",)


    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if ' ' in self.cleaned_data["fullname"].split(None, 1):
            first_name, last_name = self.cleaned_data["fullname"].split(None, 1)
            user.first_name = first_name
            user.last_name = last_name
        else:
            user.first_name = self.cleaned_data["fullname"]

        user_type = self.cleaned_data["user_type"]

        if commit:
            user.save()

        if user_type == "Company User":
            g = Group.objects.get(id=1)
            g.user_set.add(user)
        elif user_type == "Investor":
            g = Group.objects.get(id=2)
            g.user_set.add(user)

        return user


class SearchForm(forms.ModelForm):
	class Meta:
		model = Search
		fields = ('search',)
