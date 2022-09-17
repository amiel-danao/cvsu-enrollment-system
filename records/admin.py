from django.contrib import admin
from .models import Record

class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'roll', 'batch', 'department', 'Student_Contact', 'email', 'is_published')
    list_display_links = ('id', 'name')
    list_editable = ('is_published',)
    search_fields = ('name', 'roll', 'batch', 'department')
    list_per_page = 30

# Register your models here.
admin.site.register(Record, RecordAdmin)
