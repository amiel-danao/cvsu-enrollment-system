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
from django.http import JsonResponse
from django.http import HttpResponseRedirect


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
        instance = form.save(commit=False)
        instance.user = self.request.user
        form.instance.user = self.request.user
        instance.save()
        return super(RecordCreateView, self).form_valid(form)

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.user = self.request.user
    #     self.object.save()
    #     return HttpResponseRedirect(self.get_success_url())

    # def post(self, request, *args, **kwargs):
    #     form = RecordForm(request.POST)
    #     if form.is_valid():
    #         book = form.save()
    #         book.save()
    #         return HttpResponseRedirect(self.get_success_url())
    #     return render(request, 'books/book-create.html', {'form': form})

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            return JsonResponse(form.errors, status=400)

    def get_form(self, *args, **kwargs):
        try:
            latest_record = Record.objects.filter(
                user=self.request.user).order_by('school_year').reverse().first()
            if (latest_record.school_year == datetime.datetime.now().year):
                self.object = latest_record
        except (Record.DoesNotExist):
            pass

        return super().get_form(*args, **kwargs)

    def get_initial(self, *args, **kwargs):
        initial = super(RecordCreateView, self).get_initial(**kwargs)
        try:
            latest_record = Record.objects.filter(
                user=self.request.user).order_by('school_year').reverse().first()
            if (latest_record.school_year != datetime.datetime.now().year):
                initial = model_to_dict(latest_record)
        except (Record.DoesNotExist):
            pass

        return initial


class RecordUpdateView(UpdateView):
    model = Record
    fields = [field.name for field in model._meta.get_fields()
              if field.name not in ['user', 'approved']]

    def form_valid(self, form):
        instance = form.save(commit=False)
        form.instance.user = self.request.user
        instance.save()
        return super(RecordUpdateView, self).form_valid(form)


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
