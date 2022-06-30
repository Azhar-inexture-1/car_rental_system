from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """Sends mail to the user requested for password reset.
    Mail contains link with token for user identification and validation.
    Parameters
    ----------
    instance: object
        accounts.views.PasswordResetView
    sender: class `accounts.views.PasswordResetView`
    reset_password_token:
        Password reset token for user
    """
    print("Instance: ", instance)
    print("Reset_password_token: ", reset_password_token)
    print("Sender : ", sender)
    email_plaintext_message = "{}?token={}".format(
        instance.request.build_absolute_uri(reverse('password-reset-confirm')),
        reset_password_token.key
    )
    send_mail(
        # title:
        "Password Reset Link for {title}".format(title="Car Rental Account"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
