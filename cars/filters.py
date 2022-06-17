from django_filters import rest_framework as filters
from .models import Car


class CarFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    type = filters.CharFilter(field_name="type__name", lookup_expr='icontains')
    brand = filters.CharFilter(field_name="brand__name", lookup_expr='icontains')

    class Meta:
        model = Car
        fields = '__all__'
