from email.policy import default
from rest_framework import serializers
from .models import Order


class CreateOrderSerializer(serializers.ModelSerializer):

    user = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ['car', 'user', 'start_date', 'end_date', 'price']
