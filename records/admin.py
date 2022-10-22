from django.contrib import admin
from .models import Course, Department, Record, Subject


class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'middle_name', 'last_name')
    list_display_links = ('id', )
    search_fields = ('first_name', 'middle_name', 'last_name')
    list_per_page = 30
    readonly_fields = ('user',)


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
