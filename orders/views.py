from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from cars.models import Car
from .models import Order
from .serializers import CreateOrderSerializer, ReturnOrderSerializer
from rest_framework import status
from datetime import datetime, date, timedelta


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
        if start_date > end_date:
            return Response(
                {'message':'Invalid request, start date is smaller than the end date.'},
                status=status.HTTP_400_BAD_REQUEST
            )
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


class CancelOrder(APIView):
    
    def post(self, request, pk, *args, **kwargs):
        order = get_object_or_404(Order, id=pk)
        if order.canceled == True:
            return Response({'message':'Invalid request, order is already canceled.'},
            status=status.HTTP_400_BAD_REQUEST)
        elif order.start_date < date.today():
            return Response({'message':'Order cannot be canceled after the booking date.'},
            status=status.HTTP_400_BAD_REQUEST)
        order.canceled=True
        order.save()
        return Response({'message':'Order canceled successfully.'}, status=status.HTTP_200_OK)


class ReturnCarOrder(APIView):

    def post(self, request, pk, *args, **kwargs):
        order = get_object_or_404(Order, id=pk)
        today = date.today()
        if order.canceled == True or order.returned == True or today < order.start_date:
            return Response({'message':'Invalid request.'},
            status=status.HTTP_400_BAD_REQUEST)

        if order.end_date+timedelta(days=1) <= today:
            days = today - (order.end_date + timedelta(days=1))
            print(today, order.end_date, timedelta(days=1), days)
            car = Car.objects.get(id=order.car.id)
            fine_amount = days.days * car.price
            order.fine_amount = fine_amount
        
        order.returned=True
        order.save()
        serializer = ReturnOrderSerializer(order)
        return Response(
            {
                'message':'Car return successfully.',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

class ViewBookings(ListAPIView):
    serializer_class = CreateOrderSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user, returned=False)
        return queryset


class ViewBookingHistory(ListAPIView):
    serializer_class = ReturnOrderSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user, returned=True)
        return queryset
