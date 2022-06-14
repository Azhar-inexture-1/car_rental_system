from django.contrib.auth.models import (
    BaseUserManager
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
