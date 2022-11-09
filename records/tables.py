import django_tables2 as tables
from authority.views import is_all_files_ok
from records.models import Record
from django_tables2.utils import A  # alias for Accessor
from django_tables2 import TemplateColumn


class RecordsTable(tables.Table):
    edit = TemplateColumn(
        template_code='<a href="{% url "records:record-update" record.id %}" class="btn btn-primary">Edit</a>')
    # tables.LinkColumn('records:record-update', args=[A('pk')], attrs={
    #     'a': {'class': 'btn'}
    # })

    def render_approved(self, value, record):
        return "Yes" if is_all_files_ok(record) else "No"

    class Meta:
        model = Record
        fields = ('last_name', 'first_name',
                  'middle_name', 'semester', 'school_year', 'course', 'approved')
        exclude = ('home_address', 'landline_no', 'cellphone_no')
