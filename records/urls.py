from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'records'),
    path('<int:record_id>', views.record, name = 'record'),
    path('search', views.search, name = 'search')
]