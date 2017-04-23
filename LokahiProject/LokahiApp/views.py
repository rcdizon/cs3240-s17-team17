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
from .models import Message
from .forms import SendMessage
from .forms import SearchForm
from django.shortcuts import redirect
import os
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
        form = CreateReport(request.POST, request.FILES, instance=report)
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
def message(request):
    messages = Message.objects.filter(recipient = request.user)
    if request.method == "POST":
        form = SendMessage(request.POST)
        if form.is_valid():
            messenger = form.save(commit=False)
            messenger.timestamp = timezone.now()
            messenger.save()
            return redirect('sent_messages', pk=messenger.pk)
    else:
    	data = {'sender': request.user}
    	form = SendMessage(initial = data)
    return render(request, 'messenger.html', {'form': form})

@login_required(login_url='/LokahiApp/login/')
def sent_messages(request, pk):
    sent_messages = get_object_or_404(Message, pk=pk)
    return render(request, 'sent_messages.html', {'sent_messages': sent_messages})

@login_required(login_url='/LokahiApp/login/')
def inbox(request):
    inbox_messages = Message.objects.filter(recipient=request.user)
    return render(request, 'inbox.html', {'inbox_messages': inbox_messages })

@login_required(login_url='/LokahiApp/login/')
def submit(request):
    info=request.POST['info']
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    user.save()

@login_required(login_url='/LokahiApp/login/')
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
    g.user_set.add(u)
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

@login_required(login_url='/LokahiApp/login/')
def sitemanagerindex(request):
    name = request.user
    my_groups = []
    for g in Group.objects.all():
        my_groups.append(g)
    # Get list of all users, TODO: cleanup later, don't add all users to this list
    users = User.objects.all()
    return render(request, 'sitemanagerindex.html', {'name': name, 'my_groups': my_groups, "users": users})

@login_required(login_url='/LokahiApp/login/')
def search(request):
	if request.method == 'POST':
		search_request = SearchForm(request.POST)
		if search_request.is_valid():
			search_name = search_request.save()
			search_request.save()
			search_requests= Report.objects.filter(companyName = search_name)
	else:
		search_request = SearchForm()
	return render(request, 'search.html', {'search_request': search_request})





