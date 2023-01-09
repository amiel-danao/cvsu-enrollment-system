import datetime
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import login
from django.core.files.storage import FileSystemStorage
from authority.models import CustomUser
from records.forms import APPLICATION_FORM_FIELDS, APPLICATION_FORM_FIELDS_TRANSFEREE, ApplicationForm, NewUserForm, ProfilePicForm, RecordForm
from records.models import REGISTRATION_STATUS_CHOICES, STUDENT_CLASSIFICATION_CHOICES, TRANSFEREE_INDEX, FormsApproval, Record
from django.core.exceptions import BadRequest
from django.http import HttpResponse
from docx import Document
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic.detail import DetailView
from django.core import serializers
from django.forms.models import model_to_dict
from django.http import Http404


def index(request):
    if request.user is None or request.user.is_authenticated is False:
        return redirect('/accounts/login')
    context = {}
    return render(request, 'enrollment/enrollment.html', context)


def register_request(request):
    context = {}
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            #messages.success(request, "Registration successful." )
            return redirect("index")
        context['form_errors'] = form.errors
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    context["register_form"] = form
    return render(request=request, template_name="registration/register.html",  context=context)


def my_application(request):

    latest_record = Record.objects.filter(
        user=request.user).order_by('school_year').reverse().first()
    if latest_record is not None:
        latest_form_approval = FormsApproval.objects.get(record=latest_record)

        if request.method == 'POST':
            form = ApplicationForm(
                request.POST, request.FILES, instance=latest_record)
            if form.is_valid():
                form.save()
                # un-check forms that has no corresponding files
                uncheck_cleared_files(latest_record, request.FILES)

                form_approval_url = request.build_absolute_uri(
                    f'/admin/records/formsapproval/{latest_form_approval.id}/change/')
                email_message = f'This is an automated mail to remind you that a user has uploaded a form. You can see the uploaded form using this <a href="{form_approval_url}">link</a>'
                superusers_emails = CustomUser.objects.filter(
                    is_staff=True).values_list('email', flat=True)

                to_emails = list(superusers_emails)

                # superusers_emails = [
                #     'amielrenaissance4@gmail.com', 'amiel.danao@yahoo.com']
                send_mail('CVSU Enrollment-System Form Uploaded', email_message,
                          request.user.email, to_emails, fail_silently=False, html_message=email_message)
                return redirect('application')
        else:
            form = ApplicationForm(instance=latest_record)

        all_files_ok = is_all_files_ok(latest_record)

        return render(request, 'pages/application.html', {
            'form': form,
            'record': latest_form_approval,
            'all_files_ok': all_files_ok,
        })
    else:
        return render(request, 'pages/application.html')


def user_profile(request):

    record = Record.objects.filter(
        user=request.user).order_by('school_year').reverse().first()

    if record is not None and record.user.id is not request.user.id:
        raise PermissionError("Permission Denied!")

    # record_form = RecordForm(data=model_to_dict(record))
    # data = serializers.serialize("python", Record.objects.all())
    is_approved = is_all_files_ok(record)
    registration_status_value = None
    if record is not None:
        registration_status_value = [
            tup for tup in REGISTRATION_STATUS_CHOICES if record.registration_status in tup][0][1]

    context = {
        'record': record,
        'student_id': get_student_id(record),
        'registration_status': registration_status_value,
        'enrollment_status': "Approved" if is_approved else "Pending"
    }

    if request.method == 'POST':
        form = ProfilePicForm(
            request.POST, instance=request.user, files=request.FILES)

        if form.is_valid():
            userprofile = form.save()
            userprofile.save()
        else:
            context['form'] = form

    return render(request, 'authority/customuser_detail.html', context)


def uncheck_cleared_files(latest_record, files):
    try:
        latest_form_approval = FormsApproval.objects.get(record=latest_record)

        field_list = APPLICATION_FORM_FIELDS
        if latest_record.student_classification == TRANSFEREE_INDEX:
            field_list = APPLICATION_FORM_FIELDS_TRANSFEREE

        for field in field_list:
            if not getattr(latest_record, field):
                setattr(latest_form_approval, field, False)

        latest_form_approval.save()
    except Exception:
        pass


def is_all_files_ok(latest_record):
    if latest_record is None:
        return False
    field_list = APPLICATION_FORM_FIELDS
    if latest_record.student_classification == TRANSFEREE_INDEX:
        field_list = APPLICATION_FORM_FIELDS_TRANSFEREE

    try:
        latest_form_approval = FormsApproval.objects.get(record=latest_record)
        for field in field_list:
            file = getattr(latest_form_approval, field)
            if file is False:
                return False
    except Exception:
        pass
    return True


def download_form(request):
    if request.user is None or request.user.is_authenticated is False:
        return redirect('/accounts/login')

    latest_record = Record.objects.filter(
        user=request.user).order_by('school_year').reverse().first()

    if latest_record is None:
        raise Record.DoesNotExist
    document = Document()
    student_id = get_student_id(latest_record)
    document.add_heading('Registration Form Sample', 0)

    p = document.add_paragraph(student_id)
    # p.add_run('bold').bold = True
    # p.add_run(' and some ')
    # p.add_run('italic.').italic = True

    # document.add_heading('Heading, level 1', level=1)
    # document.add_paragraph('Intense quote', style='IntenseQuote')

    # document.add_paragraph(
    #     'first item in unordered list', style='ListBullet'
    # )
    # document.add_paragraph(
    #     'first item in ordered list', style='ListNumber'
    # )

    #document.add_picture('monty-truth.png', width=Inches(1.25))

    # table = document.add_table(rows=1, cols=3)
    # hdr_cells = table.rows[0].cells
    # hdr_cells[0].text = 'Qty'
    # hdr_cells[1].text = 'Id'
    # hdr_cells[2].text = 'Desc'

    # document.add_page_break()

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=registration-form.docx'
    document.save(response)

    return response


def get_student_id(record):
    if record is None:
        return 'No Student ID'
    id = record.id
    year = datetime.datetime.now().year
    semester = record.semester
    return f'{year}-{semester:02}-{id:03}'
