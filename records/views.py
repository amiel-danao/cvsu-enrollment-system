from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from records.forms import RecordForm
from records.tables import RecordsTable
from .models import Record
from records.choices import department_choices
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
import datetime


def admission(request):
    if request.user is None or request.user.is_authenticated is False:
        return redirect('/accounts/login')

    records = Record.objects.filter(user=request.user)

   #  paginator = Paginator(records, 20)
   #  page = request.GET.get('page')
   #  paged_records = paginator.get_page(page)

   #  context = {
   #      'records': paged_records
   #  }

    table = RecordsTable(records)

    return render(request, 'records/records.html', {
        "table": table
    })

   # return render(request, 'records/records.html', context)

   # Record View


def record(request, record_id):
    record = get_object_or_404(Record, pk=record_id)

    context = {
        'record': record
    }

    return render(request, 'records/record.html', context)


class RecordFormView(FormView):
    template_name = 'admission/admission.html'
    form_class = RecordForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)


class RecordCreateView(CreateView):
    model = Record
    fields = [field.name for field in model._meta.get_fields()
              if field.name not in ['user', 'approved']]


class RecordUpdateView(UpdateView):
    model = Record
    fields = '__all__'
    fields = [field.name for field in model._meta.get_fields()
              if field.name not in ['user', 'approved']]


class RecordDeleteView(DeleteView):
    model = Record
    success_url = reverse_lazy('record-list')


def get_current_semester():
    current_month = datetime.datetime.now().month
    current_semester = int((current_month / 3) + 1)
    return current_semester


def get_admission(request):
    current_semester = get_current_semester()

    return redirect('/admission/add')
