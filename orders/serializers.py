from rest_framework import serializers
from .models import Order


class CreateOrderSerializer(serializers.ModelSerializer):

    user = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ['car', 'user', 'start_date', 'end_date', 'price']


class ReturnOrderSerializer(serializers.ModelSerializer):

    user = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ['id', 'car', 'user', 'start_date', 'end_date', 'price', 'fine_amount', 'total_amount']

class OrderSerializer(serializers.ModelSerializer):

    user = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ['id', 'car', 'user', 'start_date', 'end_date', 'price']
