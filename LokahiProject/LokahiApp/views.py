# importing required packages

from django.http import Http404
from django.http import HttpResponse
from django.template import loader
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.files import File
from LokahiProject import settings
from .models import Report
from .forms import CreateReport
from django.shortcuts import redirect
import os
from django.contrib.auth.decorators import login_required

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


@login_required(login_url='/LokahiApp/login/')
def homepage(request):
    reports = Report.objects.filter(timestamp__lte=timezone.now()).order_by('timestamp')
    return render(request, 'report.html', {'reports': reports})


@login_required(login_url='/LokahiApp/login/')
def create_report(request):
    if request.method == "POST":
        form = CreateReport(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.timestamp = timezone.now()
            report.save()
            return redirect('result', pk=report.pk)
    else:
        form = CreateReport()
    return render(request, 'create_report.html', {'form': form})


@login_required(login_url='/LokahiApp/login/')
def report_edit(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == "POST":
        form = CreateReport(request.POST, instance=report)
        if form.is_valid():
            report = form.save(commit=False)
            report.timestamp = timezone.now()
            report.save()
            return redirect('result', pk=report.pk)
    else:
        form = CreateReport(instance=report)
    return render(request, 'create_report.html', {'form': form})


@login_required(login_url='/LokahiApp/login/')
def report(request):
    reports = Report.objects.filter(timestamp__lte=timezone.now()).order_by('timestamp')
    return render(request, 'report.html', {'reports': reports})


@login_required(login_url='/LokahiApp/login/')
def result(request, pk):
    reports = get_object_or_404(Report, pk=pk)
    return render(request, 'result.html', {'reports': reports})


def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT + "/media/", path)
    if os.path.exists(file_path):
        f = open(file_path, 'rb')
        file = File(f)
        response = HttpResponse(file, content_type='application/force_download')
        response['Content-Disposition'] = 'attachment; filename=%s' %smart_str(os.path.basename(file_path))
        return response
    else:
        raise Http404