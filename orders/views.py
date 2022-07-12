from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from cars.models import Car
from .models import Order
from .serializers import CreateOrderSerializer, ReturnOrderSerializer, OrderSerializer
from rest_framework import status
from datetime import datetime, date, timedelta
from constants import (
    CAR_BOOKING_NOT_AVAILABLE,
    CAR_RETURN_SUCCESS,
    INVALID_REQUEST,
    INVALID_START_END_DATE,
    INVALID_START_DATE,
    LATE_ORDER_CANCEL,
    ORDER_ALREADY_CANCELLED,
    ORDER_CANCEL_SUCCESS,
    PROVIDE_START_END_DATE, ORDER_CANCEL_FAILED,
)
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateOrder(CreateAPIView):
    """Saves car booking made by user.
    Booking is rejected if the dates overlaps existing bookings in the :model:Order.
    """
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        start_date = self.request.data.get('start_date')
        end_date = self.request.data.get('end_date')
        if start_date is None or end_date is None:
            return Response(
                {'message': PROVIDE_START_END_DATE},
                status=status.HTTP_400_BAD_REQUEST
            )
        car_id = self.request.data.get('car')
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        if start_date > end_date:
            return Response(
                {'message': INVALID_START_END_DATE},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif start_date < date.today():
            return Response(
                {'message': INVALID_START_DATE},
                status=status.HTTP_400_BAD_REQUEST
            )
        overlapping_orders = Order.objects.filter(
            car_id=car_id, cancelled=False,
            start_date__lte=end_date, end_date__gte=start_date).exists()
        if overlapping_orders:
            return Response(
                {'message': CAR_BOOKING_NOT_AVAILABLE},
                status=status.HTTP_400_BAD_REQUEST
            )
        days = end_date-start_date
        days = days.days+1
        car = Car.objects.get(id=car_id)
        data['price'] = days * car.price
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CancelOrder(APIView):
    """
    View for Cancellation of booking.
    Only allows if the booking start date is less than date of cancellation.
    """

    permission_classes = [IsAuthenticated]
    """List of permissions that should be used for granting or denial of request.
    """

    def post(self, request, pk, *args, **kwargs):
        """Accepts post requests

        Parameters
        ----------
        request: HttpRequest object
            Contains data about the request.
        pk: (int)
            Id of the :model:`order`.
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.

        Returns
        -------
        Response: objects
            Renders to content type as requested by the client.
        """
        order = get_object_or_404(Order, id=pk)
        if order.cancelled:
            return Response(
                {'message': ORDER_ALREADY_CANCELLED},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif order.start_date < date.today():
            return Response(
                {'message': LATE_ORDER_CANCEL},
                status=status.HTTP_400_BAD_REQUEST
            )
        refund = stripe.Refund.create(payment_intent=order.payment_intent_id)
        if refund["status"] == "succeeded":
            order.cancelled = True
            order.save()
            return Response({'message': ORDER_CANCEL_SUCCESS}, status=status.HTTP_200_OK)
        return Response({'message': ORDER_CANCEL_FAILED}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReturnCarOrder(APIView):
    """Order completion view.
    Fine is charged if the car is not returned within time
    """

    permission_classes = [IsAuthenticated]
    """List of permissions that should be used for granting or denial of request.
    """

    def post(self, request, pk, *args, **kwargs):
        """Accepts post requests

        Parameters
        ----------
        request: HttpRequest object
            Contains data about the request.
        pk: (int)
            Id of the :model:`order`.
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.

        Returns
        -------
        Response: objects
            Renders to content type as requested by the client.
        """
        order = get_object_or_404(Order, id=pk)
        today = date.today()
        if order.cancelled or order.returned or today < order.start_date:
            return Response(
                {'message': INVALID_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )

        if order.end_date+timedelta(days=1) <= today:
            days = today - (order.end_date + timedelta(days=1))
            days = days.days + 1
            car = Car.objects.get(id=order.car.id)
            """fine calculations
            Increasing fine per day, if fine is 5% per day then, for 3 days the total fine would be,
                5, 10, 15 -> total 30%
                considering price of car as 3000,
                fine_percent = (3000 * 30)//100 = 900
                total_fine = 3000*3 + 900 = 9900
            """
            percentage_fine = (car.price * ((((days+1) * days)//2)*5)) //100
            fine_amount = days * car.price + percentage_fine
            order.fine_amount = fine_amount
            order.fine_generated = True
        
        order.returned = True
        order.save()
        serializer = ReturnOrderSerializer(order)
        return Response(
            {
                'message': CAR_RETURN_SUCCESS,
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )


class ViewBookings(ListAPIView):
    """
    Current and new bookings view.
    """
    permission_classes = [IsAuthenticated]
    """List of permissions that should be used for granting or denial of request.
    """

    serializer_class = OrderSerializer
    """The serializer class that should be used for validating and deserializing input,
    and for serializing output.
    """

    def get_queryset(self):
        """Return queryset that should be used for returning objects from this view.
        returns
        -------
        queryset: for :model:`Order`
        """
        queryset = Order.objects.filter(user=self.request.user, returned=False)
        return queryset


class ViewBookingHistory(ListAPIView):
    """Shows previous bookings made by the user.
    """

    permission_classes = [IsAuthenticated]
    """List of permissions that should be used for granting or denial of request.
    """

    serializer_class = ReturnOrderSerializer
    """The serializer class that should be used for validating and deserializing input,
    and for serializing output.
    """

    def get_queryset(self):
        """Return queryset that should be used for returning objects from this view.
        returns
        -------
        queryset: for :model:`Order`
        """
        queryset = Order.objects.filter(user=self.request.user)
        return queryset
