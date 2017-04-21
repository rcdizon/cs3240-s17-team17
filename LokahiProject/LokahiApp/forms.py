from django import forms
from .models import Report
from .models import Message
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
        fields = ('companyName', 'companyLocation', 'companyPhone', 'companyCountry',
                  'currentProjects', 'industry', 'sector', 'upload', 'encrypted', 'privacy')

class SendMessage(forms.ModelForm):
	class Meta:
		model = Message
		fields = ('recipient','textbox','sender',)

class RegisterForm(UserCreationForm):
    fullname = forms.CharField(label="Full name")
    CHOICES = (('Company User', 'Company User'), ('Investor', 'Investor'), ('Site Manager', 'Site Manager'),)
    user_type = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = User
        fields = ("username", "fullname", "user_type",)

    '''
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        first_name, last_name = self.cleaned_data["fullname"].split(None, 1)
        user.first_name = first_name
        user.last_name = last_name

        user_type = self.cleaned_data["user_type"]
        if user_type == "Company User":
            permission = Permission.objects.get(name='isCompanyUser')
            user.user_permissions.add(permission)
        elif user_type == "Investor":
            permission = Permission.objects.get(name='isInvestor')
            user.user_permissions.add(permission)
        elif user_type == "Site Manager":
            permission = Permission.objects.get(name='isSiteManager')
            user.user_permissions.add(permission)

        if commit:
            user.save()
        return user
    '''
class SearchForm(forms.Form):
	reportDate = forms.DateTimeField()
	companyName = forms.CharField(label="Company Name")
	ceoName = forms.CharField(label="CEO Name")
	sector = forms.CharField(label="Sector")
	industry = forms.CharField(label="Industry")
	companyLocation = forms.CharField(label="Company Location")
	companyCountry = forms.CharField(label="Company Country")
	currentProjects = forms.CharField(label="Current Projects")
	filename = forms.CharField(label="Uploaded Files")