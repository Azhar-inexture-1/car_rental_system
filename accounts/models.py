from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, password2=None, **other_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **other_fields
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, phone_number, password2=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            phone_number=phone_number,
            is_staff=True,
            is_admin=True,
            is_superuser=True
        )
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Invalid phone number. Only 10 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=10)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # a admin user; non super-user
    is_admin = models.BooleanField(default=False) # a superuser

    # Password field is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number'] # Email & Password are required by default.

    objects = UserManager()

    def __str__(self):
        return self.email
