from django.contrib import admin
from .models import Authority

class AuthorityAdmin(admin.ModelAdmin):
    list_display = ('title', 'phone', 'email')
    list_display_links = ('title',)
    search_fields = ('title',)
    list_per_page = 30

# Register your models here.
admin.site.register(Authority, AuthorityAdmin)
