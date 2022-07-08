from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
import stripe

User = settings.AUTH_USER_MODEL
stripe.api_key = settings.STRIPE_SECRET_KEY


class Discount(models.Model):
    name = models.CharField(max_length=100, unique=True)
    stripe_discount_id = models.CharField(max_length=100, unique=True)
    percentage_off = models.FloatField(validators=[MinValueValidator(5.00), MaxValueValidator(100.00)], null=False, default=10)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        coupon = stripe.Coupon.create(percent_off=self.percentage_off)
        self.stripe_discount_id = coupon['id']
        super(Discount, self).save(*args, **kwargs)
