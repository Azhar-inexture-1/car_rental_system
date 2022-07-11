from django.urls import path
from .views import (
    CheckoutRender, StripeSessionView,
    StripeConfigView, SuccessView,
    CancelledView, stripe_webhook,
    ListCreateDiscount, DeleteDiscountCoupon
)

urlpatterns = [
    path('config/', StripeConfigView.as_view(), name="stripe-config"),
    path('checkout/', CheckoutRender.as_view()),
    path('checkout-session/', StripeSessionView.as_view()),
    path('success/', SuccessView.as_view()),
    path('cancel/', CancelledView.as_view()),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),

    path('create-discount-coupon/', ListCreateDiscount.as_view(), name="create-coupons"),
    path('delete-discount-coupon/', DeleteDiscountCoupon.as_view(), name="delete-coupons")
]
