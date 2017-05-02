from django.http import Http404
from django.http import HttpResponse
from django.template import loader
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.files import File
from LokahiProject import settings
from django.core.signing import Signer
from .models import Report
from .forms import CreateReport
from .models import Message
from .forms import SendMessage
from .forms import SearchForm
from .models import Search
from .forms import RegisterForm
from django.shortcuts import redirect
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import ARC4
import os
from django.views.generic import ListView
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render_to_response
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
    user = request.user
    user.save()
    if user.profile.public == '':
        random_generator = Random.new().read
        key = RSA.generate(1024, random_generator)
        public_key = key.publickey().exportKey()
        private_key = key.exportKey()
        user = request.user
        user.profile.public = public_key
        user.save()
        return render(request,'encrypt_user.html', {'private_key': private_key})
    name = request.user
    reports = Report.objects.filter(timestamp__lte=timezone.now()).order_by('timestamp')
    my_groups = []
    mutual_users = []
    for g in Group.objects.all():
        if g.id == 1 or g.id == 2 or g.id == 3:
            continue
        else:
            my_groups.append(g)
    for g in my_groups:
        for u in User.objects.filter(groups__id=g.id):
            mutual_users.append(u.id)
    return render(request, 'report.html', {'reports': reports, 'name': name, 'mutual_users': mutual_users})

@login_required(login_url='/LokahiApp/login/')
def create_report(request):
    if request.method == "POST":
        form = CreateReport(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.author = request.user
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
    my_groups = []
    mutual_users = []
    for g in Group.objects.all():
        if g.id == 1 or g.id == 2 or g.id == 3:
            continue
        else:
            my_groups.append(g)
    for g in my_groups:
        for u in User.objects.filter(groups__id=g.id):
            mutual_users.append(u.id)
    return render(request, 'report.html', {'reports': reports, 'name': name, 'mutual_users': mutual_users})


@login_required(login_url='/LokahiApp/login/')
def result(request, pk):
    reports = get_object_or_404(Report, pk=pk)
    return render(request, 'result.html', {'reports': reports})


@login_required(login_url='/LokahiApp/login/')
def message(request):
    if request.method == "POST":
        form = SendMessage(request.POST)
        encrypt_bool = request.POST.get('encrypt')
        if form.is_valid():
            messenger = form.save(commit=False)
            if encrypt_bool == None:
                messenger.set(request.user, messenger.textbox)
            else:
                reciever = messenger.recipient 
                pub_string = reciever.profile.public
                pub_key = RSA.importKey(pub_string)
                text = messenger.textbox
                messenger.textbox = pub_key.encrypt(str.encode(text), 32)
                messenger.set(request.user, messenger.textbox)
        return redirect('sent_messages', pk=messenger.pk)
    else:
        form = SendMessage()
    return render(request, 'messenger.html', {'form': form})


@login_required(login_url='/LokahiApp/login/')
def sent_messages(request, pk):
    sent_messages = get_object_or_404(Message, pk=pk)
    return render(request, 'sent_messages.html', {'sent_messages': sent_messages})


@login_required(login_url='/LokahiApp/login/')
def inbox(request):
    inbox_messages = Message.objects.filter(recipient=request.user)
    return render(request, 'inbox.html', {'inbox_messages': inbox_messages })

def individual_message(request,pk):
    message = get_object_or_404(Message, pk=pk)
    form = SendMessage(instance=message)
    return render(request, 'individual_message.html', {'form': form})

def delete_message(request,pk):
    message = get_object_or_404(Message, pk=pk)
    form = SendMessage(instance=message)
    instance = Message.objects.get(id=pk)
    instance.delete()
    inbox_messages = Message.objects.filter(recipient=request.user)
    return render(request, 'inbox.html', {'inbox_messages': inbox_messages })

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
        if g.id == 1 or g.id == 2 or g.id == 3:
            continue
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
    try:
        my_group = Group.objects.create(name=str(info))
        my_group.save()
        my_group.user_set.add(request.user)
        return render(request, 'group_successful.html', {'groups': groups, "message": "You have created and have been added to " + str(info)})
    except IntegrityError:
        return render_to_response('group_successful.html', {"message": 'A group with that name already exists.'})


@login_required(login_url='/LokahiApp/login/')
def edit_group(request, pk, qk):
    g = Group.objects.get(id=pk)
    u = User.objects.get(id=qk)
    g.user_set.add(u)
    return render(request, 'group_successful.html', {'groups': groups})


@login_required(login_url='/LokahiApp/login/')
def sm_groups(request):
    name = request.user
    my_groups = []
    for g in Group.objects.all():
        my_groups.append(g)
    # Get list of all users, TODO: cleanup later, don't add all users to this list
    users = User.objects.all()

    if request.POST.get("add"):
        g = Group.objects.get(name=request.POST.get("select"))
        u = User.objects.get(username=request.POST.get("add"))
        g.user_set.add(u)

    if request.POST.get("remove"):
        g = Group.objects.get(name=request.POST.get("select"))
        u = User.objects.get(username=request.POST.get("remove"))
        g.user_set.remove(u)
    return render(request, 'sitemanagerindex.html', {'name': name, 'my_groups': my_groups, "users": users})


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
    group_dict = {}
    for g in Group.objects.all():
        if g.id == 1 or g.id == 2 or g.id == 3:
            continue
        my_groups.append(g)
        # TODO: Later refactor, use this dict to sift out users in the respective groups
        group_dict[g] = list(User.objects.filter(groups__name=g.name))
    # Get list of all users, TODO: cleanup later, don't add all users to this list
    users = User.objects.all()
    sm_users = User.objects.filter(groups__id=1) | User.objects.filter(groups__id=2)

    return render(request, 'sitemanagerindex.html', {'name': name, 'my_groups': my_groups, "users": users, "sm_users": sm_users, "group_dict": group_dict})


@login_required(login_url='/LokahiApp/login/')
def promote_user(request):
    name = request.user
    my_groups = []
    for g in Group.objects.all():
        my_groups.append(g)
    # Get list of all users, TODO: cleanup later, don't add all users to this list
    users = User.objects.all()

    u = User.objects.get(id=request.POST.get("select"))
    u.groups.add(Group.objects.get(id=3))
    u.save()
    return render(request, 'sitemanagerindex.html', {'name': name, 'my_groups': my_groups, "users": users})


@login_required(login_url='/LokahiApp/login/')
def suspend_user(request):
    name = request.user
    my_groups = []
    for g in Group.objects.all():
        my_groups.append(g)
    # Get list of all users, TODO: cleanup later, don't add all users to this list
    users = User.objects.all()

    u = User.objects.get(id=request.POST.get("select"))
    u.is_active=False
    u.save()
    return render(request, 'sitemanagerindex.html', {'name': name, 'my_groups': my_groups, "users": users})


@login_required(login_url='/LokahiApp/login/')
def restore_user(request):
    name = request.user
    my_groups = []
    for g in Group.objects.all():
        my_groups.append(g)
    # Get list of all users, TODO: cleanup later, don't add all users to this list
    users = User.objects.all()

    u = User.objects.get(id=request.POST.get("select"))
    u.is_active=True
    u.save()
    return render(request, 'sitemanagerindex.html', {'name': name, 'my_groups': my_groups, "users": users})


@login_required(login_url='/LokahiApp/login/')
def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search_results = request.POST.get("search", "")
            results = ["Oh... No! You fucked up"] 

            for g in Report.objects.all():
                if search_results.lower() in g.companyName.lower():
                    results = Report.objects.filter(companyName__icontains = search_results)
                elif search_results.lower() in g.companyCountry.lower():
                    results = Report.objects.filter(companyCountry__icontains = search_results)
                elif search_results.lower() in g.companyLocation.lower():
                    results = Report.objects.filter(companyLocation__icontains = search_results)
                elif search_results.lower() in g.sector.lower():
                    results = Report.objects.filter(sector__icontains = search_results)
                elif search_results.lower() in g.industry.lower():
                    results = Report.objects.filter(industry__icontains = search_results)
                elif search_results.lower() in g.companyPhone.lower():
                    results = Report.objects.filter(companyPhone__icontains = search_results)
                elif search_results.lower() in g.currentProjects.lower():
                    results = Report.objects.filter(currentProjects__icontains = search_results)

            return render(request,'search.html', {'results': results} )
    else:
        form = SearchForm()
    return render(request, 'search.html', {'form': form})


@login_required(login_url='/LokahiApp/login/')
def delete_report(request, pk):
    r = Report.objects.get(id=pk)
    r.delete()

    name = request.user
    reports = Report.objects.filter(timestamp__lte=timezone.now()).order_by('timestamp')
    return render(request, 'report.html', {'reports': reports, 'name': name})
