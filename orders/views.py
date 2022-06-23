from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView
from cars.models import Car
from .models import Order
from .serializers import CreateOrderSerializer
from rest_framework import status
from datetime import datetime


class CreateOrder(CreateAPIView):
    """
    Saves car booking made by user.
    Booking is rejected if the dates overlaps existing bookings in the order table.
    """
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        start_date = self.request.data.get('start_date')
        end_date = self.request.data.get('end_date')
        car_id = self.request.data.get('car')
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        overlapping_orders = Order.objects.filter(car_id=car_id, canceled=False, start_date__lte=end_date, end_date__gte=start_date).exists()
        if overlapping_orders:
            return Response(
                {'message':'Car booking not available for given dates.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        days = end_date-start_date
        days = days.days+1
        car = Car.objects.get(id=data['car'])
        data['price'] = days * car.price
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
