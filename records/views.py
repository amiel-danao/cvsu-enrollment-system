from django.shortcuts import render, get_object_or_404
from .models import Record
from records.choices import department_choices
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.


 # index View
def index(request):
   records = Record.objects.order_by('-list_date').filter(is_published=True)

   paginator = Paginator(records, 20)
   page = request.GET.get('page')
   paged_records = paginator.get_page(page)

   context = {
      'records': paged_records
   }

   return render(request, 'records/records.html', context)


 # Record View
def record(request, record_id):
   record = get_object_or_404(Record, pk=record_id)

   context = {
      'record': record
   }

   return render(request, 'records/record.html', context)



 # Search View
def search(request):
   queryset_list = Record.objects.order_by('-list_date')

   # name
   if 'name' in request.GET:
      name = request.GET['name']
      if name:
         queryset_list = queryset_list.filter(name__icontains=name)
   # roll
   if 'roll' in request.GET:
      roll = request.GET['roll']
      if roll:
         queryset_list = queryset_list.filter(roll__icontains=roll)
   # batch
   if 'batch' in request.GET:
      batch = request.GET['batch']
      if batch:
         queryset_list = queryset_list.filter(batch__icontains=batch)
   # department
   if 'department' in request.GET:
      department = request.GET['department']
      if department:
         queryset_list = queryset_list.filter(department__iexact=department)

   context = {
      'department_choices': department_choices,
      'records': queryset_list,
      'values': request.GET
   }
   
   return render(request, 'records/search.html', context)
