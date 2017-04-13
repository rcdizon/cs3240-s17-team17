# importing required packages
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Report
from .forms import CreateReport
from .models import Message
from .forms import SendMessage
from django.shortcuts import redirect
from django.contrib.auth.models import User


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
    reports = Report.objects.filter(timestamp__lte=timezone.now()).order_by('timestamp')
    return render(request, 'report.html', {'reports': reports})


def create_report(request):
    if request.method == "POST":
        form = CreateReport(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.timestamp = timezone.now()
            report.save()
            return redirect('result', pk=report.pk)
    else:
        form = CreateReport()
    return render(request, 'create_report.html', {'form': form})


def report(request):
    reports = Report.objects.filter(timestamp__lte=timezone.now()).order_by('timestamp')
    return render(request, 'report.html', {'reports': reports})


def result(request, pk):
    reports = get_object_or_404(Report, pk=pk)
    return render(request, 'result.html', {'reports': reports})

def message(request):
    messages = Message.objects.filter(recipient = request.user)
    if request.method == "POST":
        form = SendMessage(request.POST)
        if form.is_valid():
            messenger = form.save(commit=False)
            messenger.timestamp = timezone.now()
            messenger.save(request.user)
            return redirect('sent_messages', pk=messenger.pk)
    else:
        form = SendMessage()
    return render(request, 'messenger.html', {'form': form})

def sent_messages(request, pk):
    sent_messages = get_object_or_404(Message, pk=pk)
    return render(request, 'sent_messages.html', {'sent_messages': sent_messages})

def inbox(request):
    inbox_messages = Message.objects.filter(timestamp__lte=timezone.now()).order_by('timestamp')
    return render(request, 'inbox.html', {'inbox_messages ': inbox_messages })

def submit(request):
    info=request.POST['info']
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    user.save()
