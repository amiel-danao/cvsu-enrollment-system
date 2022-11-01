from django import forms
from django.forms import ModelForm
from records.models import Record, SEMESTER_CHOICES
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.forms import UserCreationForm
from authority.models import CustomUser
from flatpickr import DatePickerInput, TimePickerInput, DateTimePickerInput
from django.forms.widgets import FileInput

APPLICATION_FORM_FIELDS = (
    'form_137',
    'card_138',
    'goodmoral',
    'notice_of_admission',
    'medical_clearance',
    'application_form',
)

APPLICATION_FORM_FIELDS_TRANSFEREE = (
    'transcript_of_record',
    'notice_of_admission',
    'medical_clearance',
    'application_form',
    'cert_of_transfer'
)


class BootstrapModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BootstrapModelForm, self).__init__(*args, **kwargs)
        # for field in iter(self.fields):
        #     self.fields[field].widget.attrs.update({
        #         'class': 'form-control'
        #     })

        self.fields['home_address'] = forms.CharField(
            label='Address',
            widget=forms.TextInput(attrs={'placeholder': '1234 Main St'})
        )
        self.fields['home_address'].widget.attrs.update(
            {'placeholder': 'House No. & Street / Barangay / Town / Province'})


class RecordForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RecordForm, self).__init__(*args, **kwargs)
        self.fields['school_elementary'].label = "Elementary"
        self.fields['school_year_elemetary'].label = "Year Graduated"
        self.fields['school_access_elementary'].label = "School type"
        self.fields['school_address_elementary'].label = "Address"

        self.fields['school_high'].label = "High School"
        self.fields['school_year_high'].label = "Year Graduated"
        self.fields['school_access_high'].label = "School type"
        self.fields['school_address_high'].label = "Address"

        self.fields['school_last_attended_address'].label = "Address"

        self.fields['parent_guardian'].label = "Parent/Guardian"
        self.fields['parent_address'].label = "Address"
        self.fields['parent_occupation'].label = "Occupation"
        self.fields['parent_landline_no'].label = "Landline No."
        self.fields['parent_cellphone_no'].label = "Cellphone No."

        self.fields['semester'].label = "Semester to enroll"
        self.fields['school_year'].label = "School year to enroll"

    class Meta:
        model = Record
        fields = [field.name for field in model._meta.get_fields()
                  if field.name not in ['user', 'approved']]
        # widgets = {
        #     'birthday': DatePickerInput(),
        # }

        # semester = forms.ChoiceField(
        #     choices=SEMESTER_CHOICES)
        # landline_no = PhoneNumberField()

        # birthday = forms.DateField(
        #     widget=forms.TextInput(
        #         attrs={'type': 'date'}
        #     )
        # )


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ApplicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields['form_137'].label = ""

    class Meta:
        model = Record
        fields = (APPLICATION_FORM_FIELDS +
                  APPLICATION_FORM_FIELDS_TRANSFEREE)
