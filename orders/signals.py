from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from accounts.models import User
from core.settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage


@receiver(post_save, sender=Order)
def send_invoice(sender, instance, created, **kwargs):
    """Sends mail to the user after creation of car booking.
    ----------
    instance: object
        Instance of :model:`orders.Order`
    sender: :model:`orders.Order`
    """
    if created:
        user = User.objects.get(id=instance.user_id)

        subject = f"Car Rental System"
        body = f"Greetings {user.first_name}, <br>\
            Your booking is confirmed <br><br>\
            <b>----------------------------------</b><br>\
            <b>Invoice </b><br>\
            <b>----------------------------------</b><br>\
            Order Id: <b>{instance.id}</b> <br>\
            Issue date: {instance.order_date} <br>\
            Customer: {user.first_name} {user.last_name} <br>\
            Amount: {instance.price} <br>\
            From: {instance.start_date} <br>\
            To: {instance.end_date} <br>\
            <b>----------------------------------</b><br><br>\
            Thank you for the order, have a safe journey."

        msg = EmailMessage(
            subject,
            body,
            EMAIL_HOST_USER,
            [user.email]
        )
        msg.content_subtype = "html"
        msg.send()
        