from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import login

from records.forms import NewUserForm


def index(request):
    if request.user is None or request.user.is_authenticated is False:
        return redirect('/accounts/login')
    context = {}
    return render(request, 'enrollment/enrollment.html', context)


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			#messages.success(request, "Registration successful." )
			return redirect("index")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render(request=request, template_name="registration/register.html", context={"register_form":form})