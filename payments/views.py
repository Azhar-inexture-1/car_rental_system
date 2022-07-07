from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import stripe
from constants import (
    CAR_BOOKING_NOT_AVAILABLE,
    INVALID_START_END_DATE,
    INVALID_START_DATE
)
from datetime import date, datetime
from rest_framework import status
from cars.models import Car
from orders.models import Order
from orders.serializers import OrderSerializer, CreateOrderSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


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
        start_date = self.request.data.get('start_date')
        end_date = self.request.data.get('end_date')
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
            car_id=car_id, canceled=False,
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
                    "name": car.reg_number,
                    "metadata": serializer.data,
                },
            },
            "quantity": 1
        }

        checkout_session = stripe.checkout.Session.create(
            success_url="http://127.0.0.1:8000/payments/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://127.0.0.1:8000/payments/cancel/",
            # payment_method_types=['card', 'gpay'],
            mode='payment',
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
        create_order(**product['metadata'])

    return HttpResponse(status=200)


def create_order(**data):
    serializer = CreateOrderSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()