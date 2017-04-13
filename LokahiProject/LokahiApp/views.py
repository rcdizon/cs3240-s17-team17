# importing required packages
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Report
from .forms import CreateReport
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import login_required
import sys

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
    name = request.user
    reports = Report.objects.filter(timestamp__lte=timezone.now()).order_by('timestamp')
    return render(request, 'report.html', {'reports': reports, 'name': name})

@login_required(login_url='/LokahiApp/login/')
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
    name = request.user
    reports = Report.objects.filter(timestamp__lte=timezone.now()).order_by('timestamp')
    return render(request, 'report.html', {'reports': reports, 'name': name})

@login_required(login_url='/LokahiApp/login/')
def result(request, pk):
    reports = get_object_or_404(Report, pk=pk)
    return render(request, 'result.html', {'reports': reports})

@login_required(login_url='/LokahiApp/login/')
def groups(request):
    # TODO: Figure out way to sort these groups properly
    name = request.user
    my_groups = []
    other_groups = []
    # Makes two lists, groups the user is in and groups the user isn't in
    for g in Group.objects.all():
        if not request.user.groups.filter(name=g.name).exists():
            other_groups.append(g)
        else:
            my_groups.append(g)
    # Get list of all users, TODO: cleanup later, don't add all users to this list
    users = User.objects.all()
    return render(request, 'groups.html', {'name': name, 'my_groups': my_groups, "other_groups": other_groups, "users": users})

@login_required(login_url='/LokahiApp/login/')
def create_group(request):
    info = request.POST['groupName']
    my_group = Group.objects.create(name=str(info))
    my_group.save()
    return render(request, 'group_successful.html', {'groups': groups})

@login_required(login_url='/LokahiApp/login/')
def edit_group(request, pk, qk):
    g = Group.objects.get(id=pk)
    u = User.objects.get(id=qk)
    g.user_set.remove(u)
    return render(request, 'group_successful.html', {'groups': groups})

@login_required(login_url='/LokahiApp/login/')
def join_group(request, pk):
    request.user.groups.add(Group.objects.get(id=pk))
    return render(request, 'group_successful.html', {'groups': groups})

@login_required(login_url='/LokahiApp/login/')
def leave_group(request, pk):
    g = Group.objects.get(id=pk)
    g.user_set.remove(request.user)
    return render(request, 'group_successful.html', {'groups': groups})
