from rest_framework import serializers
from .models import Discount


class CreateDiscountSerializer(serializers.ModelSerializer):
    """Serializer for creating discounts.
    """

    class Meta:
        model = Discount
        fields = '__all__'
        extra_kwargs = {
            'percentage_off': {'required': True},
            'stripe_discount_id': {'read_only': True}
        }
        