from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from authority.managers import CustomUserManager
from django.core.exceptions import ValidationError


def validate_image(image):
    pass
    # max_height = 512
    # max_width = 512
    # height = image.file.image.height
    # width = image.file.image.width
    # if width > max_width or height > max_height:
    #     return ValidationError("Height or Width is larger than what is allowed")


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(_("email address"), unique=True)
    picture = models.ImageField(
        upload_to='images/', blank=True, null=True, default='')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
