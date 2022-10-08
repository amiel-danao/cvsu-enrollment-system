import django_tables2 as tables
from records.models import Record


class RecordsTable(tables.Table):
    class Meta:
        model = Record
        fields = ('last_name', 'first_name',
                  'middle_name', 'semester', 'approved')
        exclude = ('home_address', 'landline_no', 'cellphone_no')
