from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.contrib.auth.password_validation import validate_password, get_password_validators
from django.core.exceptions import ValidationError
from rest_framework import exceptions


class UserManager(BaseUserManager):
    """Model manager for the customer user model, :model:`accounts.User`
    """

    def create_user(self, email, password=None, password2=None, **other_fields):
        """Creates and saves a User with the given email and password.
        Parameters
        ----------
        email: (string)
        password: (string)
        password2: (string)
        other_fields: (dict)
            -first_name: (string)
            -last_name: (string)
            -phone_number: (string) - PhoneNumberField
            -is_staff: (boolean)
            -is_admin: (boolean)
            -is_superuser: (boolean)
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **other_fields
        )
        try:
            # validate the password against existing validators
            validate_password(
                password,
                password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)
            )
        except ValidationError as e:
            # raise a validation error
            raise exceptions.ValidationError({
                'password': e.messages
            })
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, phone_number, password2=None):
        """Creates and saves a superuser with the given email and password.
        Parameters
        ----------
        email: (string)
        password: (string)
        phone_number: (string) - PhoneNumberField
        password2: (string)
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
