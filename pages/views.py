from django.shortcuts import render
from django.http import HttpResponse
from records.choices import department_choices

from records.models import Record
from authority.models import Authority

# Create your views here.
def index(request):
    records = Record.objects.all()

    context = {
        'department_choices': department_choices
    }

    return render(request, 'pages/index.html', context)

def about(request):
    authority = Authority.objects.all()

    context = {
        'authority': authority
    }
    return render(request, 'pages/about.html', context)

