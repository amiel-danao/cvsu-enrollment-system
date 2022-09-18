from django.shortcuts import render
from django.http import HttpResponse
import datetime

# Create your views here.


def index(request):
    context = {
        'current_year': datetime.datetime.now().year
    }

    return render(request, 'pages/index.html', context)


def about(request):
    context = {}
    return render(request, 'pages/about.html', context)
