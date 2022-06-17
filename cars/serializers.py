from rest_framework import serializers
from .models import (
    Type, Brand, Car
)


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class CarViewSerializer(serializers.ModelSerializer):
    type = TypeSerializer()
    brand = BrandSerializer()
    
    class Meta:
        model = Car
        fields = '__all__'


class CarCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = '__all__'
