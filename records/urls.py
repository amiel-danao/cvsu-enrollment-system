from django.urls import path
from . import views

app_name = 'records'

urlpatterns = [
    path('', views.enrollment, name='enrollment'),
    #path('<int:record_id>', views.record, name='record'),
    path('add/', views.RecordCreateView.as_view(), name='record-add'),
    path('get_enrollment/', views.get_enrollment, name='get-enrollment'),
    path('enrollment/<int:pk>/',
         views.RecordUpdateView.as_view(), name='record-update'),
    path('enrollment/<int:pk>/delete/',
         views.RecordDeleteView.as_view(), name='record-delete'),
]
