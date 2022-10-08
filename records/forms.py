from django import forms
from django.forms import ModelForm
from records.models import Record, SEMESTER_CHOICES
from phonenumber_field.formfields import PhoneNumberField


class BootstrapModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BootstrapModelForm, self).__init__(*args, **kwargs)
        self.fields['semester'] = forms.ChoiceField(
            choices=SEMESTER_CHOICES)
        self.fields['landline_no'] = PhoneNumberField()
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class RecordForm(BootstrapModelForm):
    def __init__(self, *args, **kwargs):
        super(RecordForm, self).__init__(*args, **kwargs)
        #self.fields['name'].widget.attrs.update({'placeholder': 'Enter a name'})

    class Meta:
        model = Record
        fields = '__all__'
