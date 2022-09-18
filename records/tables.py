import django_tables2 as tables
from records.models import Record


class RecordsTable(tables.Table):
    class Meta:
        model = Record
