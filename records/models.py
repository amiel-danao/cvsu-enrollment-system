import datetime
from enum import unique
from time import timezone
from unittest.util import _MAX_LENGTH
from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from authority.models import CustomUser
from django.core.validators import MaxValueValidator, MinValueValidator

SEMESTER_CHOICES = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4)
]

STUDENT_CLASSIFICATION_CHOICES = [
    (1, "New"),
    (2, "Continuing"),
    (3, "Transferee"),
    (4, "Returnee"),
    (5, "Cross Enrollee"),
    (6, "Shiftee From"),
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

    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.course_name


class Record(models.Model):
    user = models.ManyToManyField(CustomUser)
    first_name = models.CharField(default="", blank=False, max_length=50)
    middle_name = models.CharField(blank=True, max_length=50)
    last_name = models.CharField(default="", blank=False, max_length=50)
    home_address = models.CharField(default="", blank=False, max_length=150)
    landline_no = PhoneNumberField(blank=True)
    cellphone_no = PhoneNumberField(blank=True)
    email = models.EmailField(max_length=254, blank=True)
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, blank=True, null=True)
    section = models.ForeignKey(
        Section, on_delete=models.SET_NULL, blank=True, null=True
    )
    student_classification = models.PositiveIntegerField(default=1,
                                                         max_length=1, choices=STUDENT_CLASSIFICATION_CHOICES)
    shiftee_from = models.CharField(max_length=150, blank=True)
    birthday = models.DateField(default=datetime.datetime.now())
    birthplace = models.CharField(default="", blank=False, max_length=150)
    age = models.PositiveIntegerField(default=18, blank=False, validators=[
                                      MaxValueValidator(100), MinValueValidator(12)])

    semester = models.PositiveIntegerField(
        choices=SEMESTER_CHOICES, blank=False, default=1)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('records:record-update', kwargs={'pk': self.pk})
