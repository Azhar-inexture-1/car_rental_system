from django_filters import rest_framework as filters
from .models import Car


class CarFilter(filters.FilterSet):
    """filter for :model:`cars.Car`
    """

    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    """Minimum price of cars, maps with the price field
    """

    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    """Maximum price of cars, maps with the price field
    """

    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    """filtering name field, looks for containing substring in the field.
    """

    type = filters.CharFilter(field_name="type__name", lookup_expr='icontains')
    """filtering type field, looks for containing substring in the field.
    """

    brand = filters.CharFilter(field_name="brand__name", lookup_expr='icontains')
    """filtering brand field, looks for containing substring in the field.
    """

    class Meta:
        model = Car
        fields = '__all__'
