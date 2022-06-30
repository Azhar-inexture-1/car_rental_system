from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    phone_number = PhoneNumberField(null=False, blank=False, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)  # an admin user; non super-user

    # Password field is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number'] # Email & Password are required by default.

    # Selecting the Model Manager
    objects = UserManager()

    def __str__(self):
        return self.email
