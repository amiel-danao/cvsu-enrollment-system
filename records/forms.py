from django import forms
from django.forms import ModelForm
from records.models import Record, SEMESTER_CHOICES
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.forms import UserCreationForm
from authority.models import CustomUser
from flatpickr import DatePickerInput, TimePickerInput, DateTimePickerInput
from django.forms import Widget
from django.utils.safestring import mark_safe
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile


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


class PrependWidget(Widget):
    """ Widget that prepend boostrap-style span with data to specified base widget """

    def __init__(self, base_widget, data, *args, **kwargs):
        u"""Initialise widget and get base instance"""
        super(PrependWidget, self).__init__(*args, **kwargs)
        self.base_widget = base_widget(*args, **kwargs)
        self.data = data

    def render(self, name, value, attrs=None, renderer=None):
        u"""Render base widget and add bootstrap spans"""
        field = self.base_widget.render(name, value, attrs)
        # date = None
        # if value is not None:
        #     date = value.strftime("%Y-%m-%d")
        return mark_safe((
            u'<div class="input-group mb-3">'
            f'<input name="{name}" value="{value}" type="text" class="form-control dateinput flatpickr-input" placeholder="yyyy-mm-dd" aria-label="" aria-describedby="basic-addon2">'
            u'<span class="input-group-text" id="basic-addon2">yyyy-mm-dd</span>'
            u'</div>'
        ) % {'field': field, 'data': self.data})


class RecordForm(ModelForm):
    birthday = forms.DateField(required=True,
                               widget=PrependWidget(base_widget=forms.DateInput, data=""))

    def __init__(self, *args, **kwargs):
        super(RecordForm, self).__init__(*args, **kwargs)
        self.fields['birthday'].label = "Birthdate"
        self.fields['birthday'].widget.attrs['placeholder'] = "yyyy-mm-dd"

        self.fields['school_elementary'].label = "Elementary"
        self.fields['school_year_elemetary'].label = "Year Graduated"
        self.fields['school_access_elementary'].label = "School type"
        self.fields['school_address_elementary'].label = "Address"

        self.fields['school_high'].label = "High School/Senior High School"
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
        fields = [field.name for field in Record._meta.get_fields()
                  if field.name not in ['approved', 'formsapproval']]
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }

    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     if Record.objects.filter(field1=cleaned_data['user'],
    #                              field2=cleaned_data['semester'], field2=cleaned_data['school_year']).exists():
    #         raise ValidationError(
    #             'Semester and school year already exists for this problem')

    #     return cleaned_data


class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['picture']
        picture = forms.CharField(label='Image', max_length=100)

    def clean_picture(self):
        image = self.cleaned_data.get("picture")
        if not image:
            raise forms.ValidationError("No image!")
        else:
            if isinstance(image, InMemoryUploadedFile) or isinstance(image, TemporaryUploadedFile):
                if image.image.height > 512 or image.image.width > 512:
                    raise ValidationError(
                        "Height or Width is larger than what is allowed")
            else:
                if image.height > 512 or image.width > 512:
                    raise ValidationError(
                        "Height or Width is larger than what is allowed")
            return image


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
        for field_name in self.fields:
            self.fields[field_name].label = ""

    class Meta:
        model = Record
        fields = (APPLICATION_FORM_FIELDS +
                  APPLICATION_FORM_FIELDS_TRANSFEREE)
