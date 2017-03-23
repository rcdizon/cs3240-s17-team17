from django.http import HttpResponse

# Create your views


def index(request):
    return HttpResponse("<h1>Welcome to Lokahi FinTech</h1>")



