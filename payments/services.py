from rest_framework.exceptions import ValidationError
from orders.serializers import OrderSerializer
from .models import Discount
from django.conf import settings
import stripe
from cars.models import Car

stripe.api_key = settings.STRIPE_SECRET_KEY

def get_car_object(pk):
    try:
        obj = Car.objects.get(id=pk)
    except Car.DoesNotExist:
        raise ValidationError({'message': "Invalid Car id."})
    return obj

def create_order_serializer(request, start_date, end_date, car):
    data = {}
    days = end_date - start_date
    days = days.days + 1
    data['price'] = days * car.price
    data['start_date'] = start_date
    data['end_date'] = end_date
    data['car'] = car.id
    serializer = OrderSerializer(data=data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    return serializer

def discount_validator(discount_id, user):
    discounts = None
    if discount_id != "" and discount_id is not None:
        discount = Discount.objects.filter(stripe_discount_id=discount_id).first()
        if discount is not None:
            if discount.user and discount.user != user:
                raise ValidationError({'message': "Invalid Coupon Code."})
            else:
                discounts = [{
                    'coupon': discount_id,
                }]
        else:
            raise ValidationError({'message': "Invalid Coupon Code."})
    return discounts


def create_payment_session(serializer, car, discounts):
    pay_data = {
        "price_data": {
            "currency": "inr",
            "unit_amount": int(float(serializer.data['price']))*100,
            "product_data": {
                "name": f"{car.brand} {car.name} {car.reg_number}",
                "metadata":{
                    "car": serializer.data['car'],
                    "start_date": serializer.data['start_date'],
                    "end_date": serializer.data['end_date'],
                    "user": serializer.data['user'],
                    "fine": False
                }
            },
        },
        "quantity": 1
    }
    checkout_session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/payments/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="http://127.0.0.1:8000/payments/cancel/",
        mode='payment',
        discounts=discounts,
        line_items=[
            pay_data,
        ],
    )
    return checkout_session

def create_fine_payment_session(order):
    car = Car.objects.get(id=order.car.id)
    pay_data = {
        "price_data": {
            "currency": "inr",
            "unit_amount": int(order.fine_amount)*100,
            "product_data": {
                "name": f"fine for: {car.brand} {car.name} {car.reg_number}",
                "metadata": {
                    "order_id": order.id,
                    "fine": True
                }
            },
        },
        "quantity": 1
    }
    checkout_session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/payments/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="http://127.0.0.1:8000/payments/cancel/",
        mode='payment',
        line_items=[
            pay_data,
        ],
    )
    return checkout_session
