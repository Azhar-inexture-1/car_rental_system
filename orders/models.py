from django.db import models
from cars.models import Car
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Order(models.Model):
    car = models.ForeignKey(Car, null=True, on_delete=models.SET_NULL, related_name="cars_set")
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    fine_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    returned = models.BooleanField(default=False)
    order_date = models.DateField(auto_now_add=True)
    canceled = models.BooleanField(default=False)

    def __str__(self):
        return f"Order-{self.id} Car-{self.car_id} user-{self.user_id}"

    @property
    def total_amount(self):
        return self.price + self.fine_amount
        