from django.urls import path
from . import views

app_name = 'records'

urlpatterns = [
    path('', views.admission, name='admission'),
    path('<int:record_id>', views.record, name='record'),
    path('add/', views.RecordCreateView.as_view(), name='record-add'),
    path('get_admission/', views.get_admission, name='get-admission'),
    path('admission/<int:pk>/',
         views.RecordUpdateView.as_view(), name='record-update'),
    path('admission/<int:pk>/delete/',
         views.RecordDeleteView.as_view(), name='record-delete'),
]
