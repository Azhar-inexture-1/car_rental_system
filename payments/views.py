from importlib.metadata import metadata
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from django.conf import settings
import stripe
from cars.models import Car
from orders.models import Order
from orders.serializers import CreateOrderSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Discount
from .serializers import CreateDiscountSerializer
from rest_framework.permissions import IsAdminUser
from .validations import date_validation, overlapping_orders_validation, validate_order_fine
from .services import create_fine_payment_session, create_order_serializer, discount_validator, create_payment_session, get_car_object


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
    responsible to handle the requests of /checkout/ endpoint.
    """
    def post(self, request):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        car_id = request.data.get('car')
        discount_id = request.data.get('stripe_discount_id')
        
        start_date, end_date = date_validation(start_date, end_date)
        overlapping_orders_validation(car_id, start_date, end_date)
        discounts = discount_validator(discount_id, request.user)

        car = Car.objects.get(id=car_id)
        serializer = create_order_serializer(request, start_date, end_date, car)

        checkout_session = create_payment_session(serializer, car, discounts)

        return Response({'sessionId': checkout_session['id']})


class SuccessView(TemplateView):
    template_name = 'payments/success.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        session_id = self.request.GET['session_id']
        session = stripe.checkout.Session.retrieve(session_id)
        payment_intent = stripe.checkout.Session.list(
                                                    payment_intent=session["payment_intent"],
                                                    expand=['data.line_items']
                                                    )
        product_id = payment_intent['data'][0]['line_items']['data'][0]['price']['product']
        product = stripe.Product.retrieve(product_id)
        context['product'] = product['metadata']
        return context


class CancelledView(TemplateView):
    template_name = 'payments/cancelled.html'


class StripeSessionView(APIView):
    """StripeSessionView is the API of sessions resource, and
    responsible to handle the requests of /pay-fine/ endpoint.
    """
    def post(self, request):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        car_id = request.data.get('car')
        discount_id = request.data.get('stripe_discount_id')
        
        start_date, end_date = date_validation(start_date, end_date)
        overlapping_orders_validation(car_id, start_date, end_date)
        discounts = discount_validator(discount_id, request.user)
        car = get_car_object(car_id)
        serializer = create_order_serializer(request, start_date, end_date, car)

        checkout_session = create_payment_session(serializer, car, discounts)

        return Response({'sessionId': checkout_session['id']})


class StripeFineSessionView(APIView):
    """StripeSessionView is the API of sessions resource, and
    responsible to handle the requests of /pay-fine/ endpoint.
    """
    def post(self, request, pk):
        order = Order.objects.get(id=pk)
        validate_order_fine(order)
        checkout_session = create_fine_payment_session(order)

        return Response({'url': checkout_session.url})


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
        print(product)
        if product['metadata']['fine'] == "True":
            order_id = product['metadata']['order_id']
            order = Order.objects.get(id=order_id)
            order.fine_paid=True
            order.fine_payment_intent_id = session["payment_intent"]
            order.save()
        else:
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
