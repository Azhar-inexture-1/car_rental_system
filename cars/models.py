from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=150, unique=True)


class Type(models.Model):
    name = models.CharField(max_length=150, unique=True)


class Car(models.Model):
    FUEL_TYPE_CHOICES = (
        (1, "Petrol"),
        (2, "Diesel"),
        (3, "Gas"),
        (4, "Electric"),
    )
    TRANSMISSION_TYPE_CHOICE = (
        (1, "Manual"),
        (2, "Automatic"),
    )
    name = models.CharField(max_length=150)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    seats = models.IntegerField(default=4)
    fuel_type = models.IntegerField(choices=FUEL_TYPE_CHOICES, default=1)
    transmission_type = models.IntegerField(choices=TRANSMISSION_TYPE_CHOICE, default=1)
    reg_number = models.CharField(max_length=20)
    available = models.BooleanField(default=False)