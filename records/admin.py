from django.contrib import admin
from .models import Record


class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'middle_name', 'last_name')
    list_display_links = ('id', )
    search_fields = ('first_name', 'middle_name', 'last_name')
    list_per_page = 30


# Register your models here.
admin.site.register(Record, RecordAdmin)
