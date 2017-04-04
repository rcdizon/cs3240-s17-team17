# importing required packages
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.utils import timezone
from .models import Report

# disabling csrf (cross site request forgery)
@csrf_exempt
def index(request):
        # if post request is not true
        # returing the form template
        template = loader.get_template('index.html')
        return HttpResponse(template.render())

def login(request):
    # if post request came
    if request.method == 'POST':
        # getting values from post
        email = request.POST.get('email')
        password = request.POST.get('password')

        # adding the values in a context variable
        context = {
            'email': email,
            'password': password
        }

        # getting our showdata template
        template = loader.get_template('LoginForm.html')

        # returing the template
        return HttpResponse(template.render(context, request))

    else: 
        # if post request is not true
        # returing the form template
        template = loader.get_template('login.html')
        return HttpResponse(template.render())


def homepage(request):
        template = loader.get_template('homepage.html')
        return HttpResponse(template.render())


def create_report(request):
        template = loader.get_template('create_report.html')
        return HttpResponse(template.render())


def report(request):
    reports = Report.objects.filter(timestamp__lte=timezone.now()).order_by('timestamp')
    return render(request, 'report.html', {'reports': reports})




