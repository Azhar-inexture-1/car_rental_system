from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=150, unique=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id}-{self.name}"


class Type(models.Model):
    name = models.CharField(max_length=150, unique=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id}-{self.name}"


class Car(models.Model):
    FUEL_TYPE_CHOICES = (
        ("petrol", "petrol"),
        ("diesel", "diesel"),
        ("gas", "gas"),
        ("electric", "electric"),
    )
    TRANSMISSION_TYPE_CHOICE = (
        ("manual", "manual"),
        ("automatic", "automatic"),
    )
    name = models.CharField(max_length=150)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    seats = models.IntegerField(default=4)
    fuel_type = models.CharField(max_length=10, choices=FUEL_TYPE_CHOICES, default="petrol")
    transmission_type = models.CharField(max_length=10, choices=TRANSMISSION_TYPE_CHOICE, default="manual")
    reg_number = models.CharField(max_length=20)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id} - {self.name}"