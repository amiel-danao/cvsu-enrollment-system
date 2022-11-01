from django.contrib import admin

from records.forms import APPLICATION_FORM_FIELDS, APPLICATION_FORM_FIELDS_TRANSFEREE
from .models import Course, Department, FormsApproval, Record, Subject
from django.forms import ModelForm


@admin.register(FormsApproval)
class FormsApprovalAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class RecordAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['forms_approval'].disabled = True
        self.fields['forms_approval'].widget.can_change_related = False

    class Meta:
        model = Record
        fields = '__all__'


class RecordAdmin(admin.ModelAdmin):
    form = RecordAdminForm
    list_display = ('id', 'first_name', 'middle_name',
                    'last_name', 'school_year')
    list_display_links = ('id', )
    search_fields = ('first_name', 'middle_name', 'last_name', 'school_year')
    list_per_page = 30
    readonly_fields = ('user', )


# Register your models here.
admin.site.register(Record, RecordAdmin)


class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'course_abbr')
    list_display_links = ('course_name', )
    search_fields = ('course_abbr', 'course_name')
    filter_horizontal = ("subjects",)


# Register your models here.
admin.site.register(Course, CourseAdmin)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_name', 'unit')
    list_display_links = ('subject_name', )
    search_fields = ('subject_name', 'unit')


# Register your models here.
admin.site.register(Subject, SubjectAdmin)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass
