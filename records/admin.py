from django.contrib import admin

from .models import Course, Department, FormsApproval, Record, Section, Subject
from django.forms import ModelForm
from admin_interface.models import Theme
from django.contrib.auth.models import Group

admin.site.unregister(Theme)
admin.site.unregister(Group)


class FormsApprovalAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['record'].disabled = True
        self.fields['record'].widget.can_change_related = False

    class Meta:
        model = FormsApproval
        fields = '__all__'


@admin.register(FormsApproval)
class FormsApprovalAdmin(admin.ModelAdmin):
    form = FormsApprovalAdminForm

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'middle_name',
                    'last_name', 'school_year')
    list_display_links = ('id', )
    search_fields = ('first_name', 'middle_name', 'last_name', 'school_year')
    list_per_page = 30
    exclude = ('registration_date', )
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


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    pass
