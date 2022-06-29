from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from orders.models import Order
from .permissions import (
    IsAdminOrReadOnly
)
from .filters import CarFilter
from .models import (
    Type, Brand, Car
)
from .serializers import (
    TypeSerializer,
    BrandSerializer,
    CarViewSerializer,
    CarCreateSerializer
)
from datetime import datetime, date
from rest_framework import status
from django.db.models import Q
from constants import (
    DELETE_BRAND_EXISTING_BOOKINGS,
    DELETE_CAR_EXISTING_BOOKINGS,
    DELETE_SUCCESS,
    DELETE_TYPE_EXISTING_BOOKINGS,
    INVALID_START_DATE,
    INVALID_START_END_DATE,
    UPDATE_SUCCESS,
)


class ListCreateTypeAPIView(ListCreateAPIView):
    """
    List all available car types and create new car types
    """
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    permission_classes = [IsAdminOrReadOnly]


class TypeRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update and Delete car types
    """
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    permission_classes = [IsAdminOrReadOnly]

    def patch(self, request, *args, **kwargs):
        response = super(TypeRetrieveUpdateDestroyAPIView, self).partial_update(request, *args, **kwargs)
        return Response(
            {"data": response.data, "message": UPDATE_SUCCESS},
            status=response.status_code
        )

    def delete(self, request, *args, **kwargs):
        if Order.objects.filter(returned=False, car__type=kwargs['pk']).exists():
            return Response(
                {"status": "OK", "message": DELETE_TYPE_EXISTING_BOOKINGS},
                status=status.HTTP_400_BAD_REQUEST
            )
        response = super(TypeRetrieveUpdateDestroyAPIView, self).destroy(request, *args, **kwargs)
        return Response(
            {"status": "OK", "message": DELETE_SUCCESS},
            status=response.status_code
        )


class ListCreateBrandAPIView(ListCreateAPIView):
    """
    List all available car brands and create new car brands
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminOrReadOnly]


class BrandRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update and Delete car brands
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminOrReadOnly]

    def patch(self, request, *args, **kwargs):
        response = super(BrandRetrieveUpdateDestroyAPIView, self).partial_update(request, *args, **kwargs)
        return Response(
            {"data": response.data, "message": UPDATE_SUCCESS},
            status=response.status_code
        )

    def delete(self, request, *args, **kwargs):
        if Order.objects.filter(returned=False, car__brand=kwargs['pk']).exists():
            return Response(
                {"status": "OK", "message": DELETE_BRAND_EXISTING_BOOKINGS},
                status=status.HTTP_400_BAD_REQUEST
            )
        response = super(BrandRetrieveUpdateDestroyAPIView, self).destroy(request, *args, **kwargs)
        return Response(
            {"status": "OK", "message": DELETE_SUCCESS},
            status=response.status_code
        )


class ListCreateCarAPIView(ListCreateAPIView):
    """
    List all available cars with filter and create new cars
    """
    queryset = Car.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = CarFilter

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        """
        if self.request.method == "GET":
            return CarViewSerializer
        return CarCreateSerializer

    def get_queryset(self):
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date is not None and end_date is not None:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            if start_date > end_date:
                raise ValidationError({
                    'message': INVALID_START_END_DATE
                })
            elif start_date < date.today():
                raise ValidationError({
                    'message': INVALID_START_DATE
                })
            overlapping_cars_id = Order.objects.filter(
                                                        canceled=False,
                                                        start_date__lte=end_date,
                                                        end_date__gte=start_date
                                                    ).values('car')
            queryset = Car.objects.exclude( 
                Q(id__in=overlapping_cars_id) |
                Q(available=False) |
                Q(brand__available=False) |
                Q(type__available=False)
            ).order_by('id')
        else:
            queryset = Car.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        response = super(ListCreateCarAPIView, self).get(request, *args, **kwargs)
        return Response(
            response.data,
            status=response.status_code
        )


class CarRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update and Delete cars
    """
    queryset = Car.objects.all()
    serializer_class = CarCreateSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        """
        if self.request.method == "GET":
            return CarViewSerializer
        return CarCreateSerializer

    def patch(self, request, *args, **kwargs):
        response = super(CarRetrieveUpdateDestroyAPIView, self).partial_update(request, *args, **kwargs)
        return Response(
            {"data": response.data, "message": UPDATE_SUCCESS},
            status=response.status_code
        )

    def delete(self, request, *args, **kwargs):
        if Order.objects.filter(returned=False, car=kwargs['pk']).exists():
            return Response(
                {"status": "OK", "message": DELETE_CAR_EXISTING_BOOKINGS},
                status=status.HTTP_400_BAD_REQUEST
            )
        response = super(CarRetrieveUpdateDestroyAPIView, self).destroy(request, *args, **kwargs)
        return Response(
            {"status": "OK", "message": DELETE_SUCCESS},
            status=response.status_code
        )
