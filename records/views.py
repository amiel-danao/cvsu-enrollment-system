from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from records.forms import RecordForm
from records.tables import RecordsTable
from .models import FormsApproval, Record
from records.choices import department_choices
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
import datetime
from django.forms.models import model_to_dict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


def enrollment(request):
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


def record(request, record_id):
    record = get_object_or_404(Record, pk=record_id)

    context = {
        'record': record
    }

    return render(request, 'records/record.html', context)


class RecordFormView(FormView):
    template_name = 'enrollment/enrollment.html'
    form_class = RecordForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)


class RecordCreateView(LoginRequiredMixin, CreateView):
    model = Record
    form_class = RecordForm
    success_url = reverse_lazy('records:enrollment')

    def form_valid(self, form):
        form.instance.user = self.request.user
        if form.instance.forms_approval is None:
            form.instance.forms_approval = FormsApproval.objects.create()
        return super(RecordCreateView, self).form_valid(form)

    def get_form(self, *args, **kwargs):
        try:
            latest_record = Record.objects.latest('school_year')
            if (latest_record.school_year == datetime.datetime.now().year):
                self.object = latest_record
        except (Record.DoesNotExist):
            pass

        return super().get_form(*args, **kwargs)

    def get_initial(self, *args, **kwargs):
        initial = super(RecordCreateView, self).get_initial(**kwargs)
        try:
            latest_record = Record.objects.latest('school_year')
            if (latest_record.school_year != datetime.datetime.now().year):
                initial = model_to_dict(latest_record)
        except (Record.DoesNotExist):
            pass

        return initial


class RecordUpdateView(UpdateView):
    model = Record
    fields = [field.name for field in model._meta.get_fields()
              if field.name not in ['user', 'approved']]


class RecordDeleteView(DeleteView):
    model = Record
    success_url = reverse_lazy('record-list')


def get_current_semester():
    current_month = datetime.datetime.now().month
    current_semester = int((current_month / 3) + 1)
    return current_semester


def get_enrollment(request):
    current_semester = get_current_semester()

    return redirect('/enrollment/add')
