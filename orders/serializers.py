import imp
from rest_framework import serializers
from .models import Order
from accounts.models import User


class CreateOrderSerializer(serializers.ModelSerializer):
    """Creates new order for :model:Order
    """

    user = serializers.CharField(default=serializers.CurrentUserDefault())
    """User field for :model:Order autofill using CurrentUserDefault function
    """

    class Meta:
        model = Order
        fields = ['car', 'user', 'start_date', 'end_date', 'price']


class ReturnOrderSerializer(serializers.ModelSerializer):
    """Serializer for returning the order.
    """

    user = serializers.CharField(default=serializers.CurrentUserDefault())
    """User field for :model:Order autofill using CurrentUserDefault function
    """

    class Meta:
        model = Order
        fields = ['id', 'car', 'user', 'start_date', 'end_date', 'price', 'fine_amount', 'total_amount']


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for viewing existing bookings.
    """

    user = serializers.CharField(default=serializers.CurrentUserDefault())
    """User field for :model:Order autofill using CurrentUserDefault function
    """

    class Meta:
        model = Order
        fields = ['id', 'car', 'user', 'start_date', 'end_date', 'price']


class CreateOrderSerializer(serializers.ModelSerializer):
    """Serializer for viewing existing bookings.
    """

    class Meta:
        model = Order
        fields = ['id', 'car', 'user', 'start_date', 'end_date', 'price']
