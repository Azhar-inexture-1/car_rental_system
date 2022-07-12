from rest_framework.exceptions import ValidationError
from datetime import datetime, date
from constants import (
    CAR_BOOKING_NOT_AVAILABLE,
    INVALID_START_DATE,
    INVALID_START_END_DATE,
    PROVIDE_START_END_DATE
)
from orders.models import Order

def date_validation(start_date, end_date):
    if start_date is None or end_date is None:
        raise ValidationError({
            "message": PROVIDE_START_END_DATE
        })
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    if start_date > end_date:
        raise ValidationError({
            "message": INVALID_START_END_DATE
        })
    elif start_date < date.today():
        raise ValidationError({
            "message": INVALID_START_DATE
        })
    return start_date, end_date
        

def overlapping_orders_validation(car_id, start_date, end_date):
    overlapping_orders = Order.objects.filter(
        car_id=car_id, cancelled=False,
        start_date__lte=end_date, end_date__gte=start_date).exists()
    if overlapping_orders:
        raise ValidationError({
            "message": CAR_BOOKING_NOT_AVAILABLE
        })


def validate_order_fine(order):
    if not order.fine_generated:
        raise ValidationError({
            "message": "Invalid request, no fine generated on this order."
        })
    elif order.fine_paid:
        raise ValidationError({
            "message": "Invalid request, fine amount already paid."
        })
