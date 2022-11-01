from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import login
from django.core.files.storage import FileSystemStorage
from records.forms import ApplicationForm, NewUserForm
from records.models import Record
from django.core.exceptions import SuspiciousOperation


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
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="registration/register.html", context={"register_form": form})


def my_account(request):

    # files_count = len(request.FILES)
    # if request.method == 'POST' and files_count > 0:
    #     for file in request.FILES:
    #         if request.FILES[file]:
    #             myfile = request.FILES[file]
    #             fs = FileSystemStorage()
    #             filename = fs.save(myfile.name, myfile)
    #             uploaded_file_url = fs.url(filename)

    #             setattr(record, file, changes.get(file))

    #     return render(request, 'pages/account.html', {
    #         'uploaded_file_url': uploaded_file_url
    #     })

    latest_record = Record.objects.latest('school_year')

    if latest_record is None:
        return render(request, 'pages/account.html')
    else:
        if request.method == 'POST':
            form = ApplicationForm(
                request.POST, request.FILES, instance=latest_record)
            if form.is_valid():
                form.save()
                # for file in request.FILES:
                #     setattr(latest_record, file, 'BAR')
                # latest_record.save()
                return redirect('myaccount')
        else:
            form = ApplicationForm(instance=latest_record)

        return render(request, 'pages/account.html', {
            'form': form,
            'record': latest_record.forms_approval
        })
