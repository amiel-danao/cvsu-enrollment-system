from django.shortcuts import render
from django.shortcuts import redirect


def index(request):
    if request.user is None or request.user.is_authenticated is False:
        return redirect('/accounts/login')
    context = {}
    return render(request, 'enrollment/enrollment.html', context)
