from rest_framework import serializers
from .models import Order


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
        fields = [
            'id', 'car', 'user', 'start_date', 'end_date',
            'price', 'fine_amount', 'total_amount', 'discount',
            'cancelled', 'refund', 'returned', 'fine_generated',
            'payment_intent_id', 'fine_paid', 'fine_payment_intent_id'
        ]
        extra_kwargs = {
            'cancelled': {'read_only': True},
            'refund': {'read_only': True},
            'returned': {'read_only': True},
            'payment_intent_id': {'read_only': True},
            'fine_generated': {'read_only': True},
            'fine_paid': {'read_only': True},
            'fine_payment_intent_id': {'read_only': True},
        }

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
        fields = [
            'id', 'car', 'user', 'start_date', 'end_date', 'price', 'discount', 'payment_intent_id'
        ]
