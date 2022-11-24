import datetime
from enum import unique
from time import timezone
from unittest.util import _MAX_LENGTH
from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from authority.models import CustomUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import signals


TRANSFEREE_INDEX = 3

SEMESTER_CHOICES = [
    (1, 1),
    (2, 2),
]

YEAR_LEVEL_CHOICES = [
    (1, "1st"),
    (2, "2nd"),
    (3, "3rd"),
    (4, "4th"),
]

STUDENT_CLASSIFICATION_CHOICES = [
    (1, "New"),
    (2, "Continuing"),
    (TRANSFEREE_INDEX, "Transferee"),
    (4, "Returnee"),
    (5, "Cross Enrollee"),
    (6, "Shiftee From"),
]

REGISTRATION_STATUS_CHOICES = [
    (1, "Regular"),
    (2, "Irregular"),
    (3, "Temporary")
]

SEX_CHOICES = [
    (1, "Male"),
    (2, "Female")
]

SCHOOL_TYPE_CHOICES = [
    (1, "Private"),
    (2, "Public")
]


class Section(models.Model):
    id = models.BigAutoField(db_column="id", primary_key=True)
    section_name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.section_name


class Department(models.Model):
    id = models.BigAutoField(db_column="dept_id", primary_key=True)
    name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.name


class Subject(models.Model):
    subject_name = models.CharField(max_length=50)
    unit = models.IntegerField()

    def __str__(self):
        return self.subject_name


class Course(models.Model):
    id = models.BigAutoField(db_column="course_id", primary_key=True)
    course_name = models.CharField(unique=True, max_length=100)
    course_abbr = models.CharField(
        db_column="course_abbr", max_length=20, blank=True, default=""
    )
    course_department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        db_column="course_department_id",
        null=True,
    )
    course_credit = models.PositiveSmallIntegerField()

    subjects = models.ManyToManyField(Subject, blank=True)

    def __str__(self):
        return self.course_name


class Record(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(default="", blank=False, max_length=50)
    middle_name = models.CharField(blank=True, max_length=50)
    last_name = models.CharField(default="", blank=False, max_length=50)
    home_address = models.CharField(default="", blank=False, max_length=150)
    landline_no = PhoneNumberField(blank=True, region="PH")
    cellphone_no = PhoneNumberField(blank=True, region="PH")
    email = models.EmailField(max_length=254, blank=True)
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, blank=True, null=True)
    section = models.ForeignKey(
        Section, on_delete=models.SET_NULL, blank=True, null=True
    )
    student_classification = models.PositiveIntegerField(
        default=1, choices=STUDENT_CLASSIFICATION_CHOICES)
    registration_status = models.PositiveIntegerField(
        default=1, choices=REGISTRATION_STATUS_CHOICES)
    shiftee_from = models.CharField(max_length=150, blank=True)
    birthday = models.DateField(default=datetime.datetime.now())
    birthplace = models.CharField(default="", blank=False, max_length=150)
    age = models.PositiveIntegerField(default=18, blank=False, validators=[
                                      MaxValueValidator(100), MinValueValidator(12)])
    sex = models.PositiveIntegerField(default=1, choices=SEX_CHOICES)
    religion = models.CharField(default="", blank=True, max_length=50)
    nationality = models.CharField(default="", blank=True, max_length=50)
    civil_status = models.CharField(default="", blank=True, max_length=50)

    school_elementary = models.CharField(
        default="", blank=True, max_length=150)
    school_year_elemetary = models.PositiveIntegerField(default=datetime.datetime.now().year, blank=True, validators=[
        MaxValueValidator(3000), MinValueValidator(1985)])
    school_access_elementary = models.PositiveIntegerField(
        default=1, choices=SCHOOL_TYPE_CHOICES)
    school_address_elementary = models.CharField(
        default="", blank=True, max_length=150)

    school_high = models.CharField(default="", blank=True, max_length=150)
    school_year_high = models.PositiveIntegerField(default=datetime.datetime.now().year, blank=True, validators=[
        MaxValueValidator(3000), MinValueValidator(1985)])
    school_access_high = models.PositiveIntegerField(
        default=1, choices=SCHOOL_TYPE_CHOICES)
    school_address_high = models.CharField(
        default="", blank=True, max_length=150)

    school_last_attended = models.CharField(
        default="", blank=True, max_length=150)
    school_last_attended_address = models.CharField(
        default="", blank=True, max_length=150)

    parent_guardian = models.CharField(default="", blank=True, max_length=50)
    parent_address = models.CharField(default="", blank=True, max_length=150)
    parent_occupation = models.CharField(default="", blank=True, max_length=50)
    parent_landline_no = PhoneNumberField(blank=True, region="PH")
    parent_cellphone_no = PhoneNumberField(blank=True, region="PH")

    year_level = models.PositiveIntegerField(
        choices=YEAR_LEVEL_CHOICES, blank=False, default=1)
    school_year = models.PositiveIntegerField(default=datetime.datetime.now().year, blank=False, validators=[
        MaxValueValidator(3000), MinValueValidator(2000)])
    semester = models.PositiveIntegerField(
        choices=SEMESTER_CHOICES, blank=False, default=1)
    approved = models.BooleanField(default=False)

    form_137 = models.FileField(
        blank=True, upload_to='documents/')

    card_138 = models.FileField(
        blank=True, upload_to='documents/')

    goodmoral = models.FileField(
        blank=True, upload_to='documents/')

    notice_of_admission = models.FileField(
        blank=True, upload_to='documents/')

    medical_clearance = models.FileField(
        blank=True, upload_to='documents/')

    application_form = models.FileField(
        blank=True, upload_to='documents/')

    transcript_of_record = models.FileField(
        blank=True, upload_to='documents/')

    notice_of_admission = models.FileField(
        blank=True, upload_to='documents/')

    cert_of_transfer = models.FileField(
        blank=True, upload_to='documents/')

    class Meta:
        unique_together = ('user', 'semester', 'school_year')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('records:record-update', kwargs={'pk': self.pk})

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set added_by during the first save.
            obj.user = request.user
        super().save_model(request, obj, form, change)


class FormsApproval(models.Model):
    record = models.ForeignKey(
        Record, on_delete=models.CASCADE)

    form_137 = models.BooleanField(default=False)
    card_138 = models.BooleanField(default=False)
    goodmoral = models.BooleanField(default=False)
    notice_of_admission = models.BooleanField(default=False)
    medical_clearance = models.BooleanField(default=False)
    application_form = models.BooleanField(default=False)
    transcript_of_record = models.BooleanField(default=False)
    notice_of_admission = models.BooleanField(default=False)
    cert_of_transfer = models.BooleanField(default=False)

    def __str__(self):
        return f'Forms Approval {self.id}'


def create_forms_approval(sender, instance, created, **kwargs):
    if created:
        FormsApproval.objects.create(record=instance)


signals.post_save.connect(create_forms_approval, sender=Record, weak=False,
                          dispatch_uid='models.create_forms_approval')
