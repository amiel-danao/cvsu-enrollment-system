from django.db import models
from django.urls import reverse

from authority.models import CustomUser

SEMESTER_CHOICES = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4)
]


class Record(models.Model):
    user = models.ManyToManyField(CustomUser)
    first_name = models.CharField(default="", blank=False, max_length=50)
    middle_name = models.CharField(blank=True, max_length=50)
    last_name = models.CharField(default="", blank=False, max_length=50)
    semester = models.PositiveIntegerField(
        choices=SEMESTER_CHOICES, blank=False, default=1)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('records:record-update', kwargs={'pk': self.pk})
