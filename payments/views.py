from importlib.metadata import metadata
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from django.conf import settings
import stripe
from constants import (
    CAR_BOOKING_NOT_AVAILABLE,
    INVALID_START_END_DATE,
    INVALID_START_DATE,
    PROVIDE_START_END_DATE
)
from datetime import date, datetime
from rest_framework import status
from cars.models import Car
from orders.models import Order
from orders.serializers import OrderSerializer, CreateOrderSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Discount
from .serializers import CreateDiscountSerializer
from rest_framework.permissions import IsAdminUser


stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeConfigView(APIView):
    """StripeConfigView is the API of configs resource, and
    responsible to handle the requests of /config/ endpoint.
    """

    def get(self, request):
        config = {
            "publishable_key": str(settings.STRIPE_PUBLISHABLE_KEY)
        }
        return Response(config)


class CheckoutRender(TemplateView):
    template_name = "payments/order.html"


class StripeSessionView(APIView):
    """StripeSessionView is the API of sessions resource, and
    responsible to handle the requests of /session/ endpoint.
    """
    def post(self, request):
        data = request.data.copy()
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date is None or end_date is None:
            return Response(
                {'message': PROVIDE_START_END_DATE},
                status=status.HTTP_400_BAD_REQUEST
            )

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
        car_id = data.get('car')
        overlapping_orders = Order.objects.filter(
            car_id=car_id, cancelled=False,
            start_date__lte=end_date, end_date__gte=start_date).exists()
        if overlapping_orders:
            return Response(
                {'message': CAR_BOOKING_NOT_AVAILABLE},
                status=status.HTTP_400_BAD_REQUEST
            )
        days = end_date - start_date
        days = days.days + 1
        car = Car.objects.get(id=car_id)
        data['price'] = days * car.price
        data['start_date'] = start_date
        data['end_date'] = end_date
        data['car'] = car_id
        serializer = OrderSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        pay_data = {
            "price_data": {
                "currency": "inr",
                "unit_amount": int(data['price'])*100,
                "product_data": {
                    "name": f"{car.brand} {car.name} {car.reg_number}",
                    "metadata": serializer.data,
                },
            },
            "quantity": 1
        }
        discount_id = data.get('stripe_discount_id')
        discounts = None
        if discount_id != "" and discount_id is not None:
            discount = Discount.objects.filter(stripe_discount_id=discount_id).first()
            if discount is not None:
                if discount.user and discount.user != request.user:
                    return Response({'message': "Invalid Coupon Code."}, status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    discounts = [{
                        'coupon': discount_id,
                    }]
            else:
                return Response({'message': "Invalid Coupon Code."}, status=status.HTTP_406_NOT_ACCEPTABLE)
        checkout_session = stripe.checkout.Session.create(
            success_url=settings.DOMAIN + "/payments/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=settings.DOMAIN + "/payments/cancel/",
            mode='payment',
            discounts=discounts,
            line_items=[
                pay_data,
            ],
        )
        return Response({'sessionId': checkout_session['id']})


class SuccessView(TemplateView):
    template_name = 'payments/success.html'

    def get(self, request, *args, **kwargs):
        # print(request.GET)
        # session_id = request.GET['session_id']
        # session = stripe.checkout.Session.retrieve(session_id)
        # sessions = stripe.checkout.Session.list(payment_intent='pi_xxx', expand=['data.line_items'])
        # print(session)
        return super(SuccessView, self).get(self, request, *args, **kwargs)


class CancelledView(TemplateView):
    template_name = 'payments/cancelled.html'


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        payment_intent = stripe.checkout.Session.list(
                                                      payment_intent=session["payment_intent"],
                                                      expand=['data.line_items']
                                                     )
        product_id = payment_intent['data'][0]['line_items']['data'][0]['price']['product']
        product = stripe.Product.retrieve(product_id)
        product['metadata']['price'] = session['amount_total']//100
        product['metadata']['discount'] = session['total_details']['amount_discount']//100
        product['metadata']['payment_intent_id'] = session["payment_intent"]
        create_order(**product['metadata'])

    if event['type'] == "charge.refunded":
        session = event['data']['object']
        order = Order.objects.get(payment_intent_id=session["payment_intent"])
        order.refund = True
        order.save()

    return HttpResponse(status=200)


def create_order(**data):
    serializer = CreateOrderSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()


class ListCreateDiscount(ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CreateDiscountSerializer
    queryset = Discount.objects.all()

    def post(self, request, *args, **kwargs):
        response = super(ListCreateDiscount, self).post(request, *args, **kwargs)
        data = response.data
        stripe.Coupon.create(
            percent_off=data.get('percentage_off'),
            metadata=data
        )
        return response


class DeleteDiscountCoupon(DestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CreateDiscountSerializer
    queryset = Discount.objects.all()
