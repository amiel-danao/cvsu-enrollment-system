import django_tables2 as tables
from records.models import Record
from django_tables2.utils import A  # alias for Accessor
from django_tables2 import TemplateColumn


class RecordsTable(tables.Table):
    edit = TemplateColumn(
        template_code='<a href="{% url "records:record-update" record.id %}" class="btn btn-primary">Edit</a>')
    # tables.LinkColumn('records:record-update', args=[A('pk')], attrs={
    #     'a': {'class': 'btn'}
    # })

    class Meta:
        model = Record
        fields = ('last_name', 'first_name',
                  'middle_name', 'semester', 'school_year', 'course', 'approved')
        exclude = ('home_address', 'landline_no', 'cellphone_no')
