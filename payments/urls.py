from django.urls import path
from .views import CheckoutRender, StripeSessionView, StripeConfigView, SuccessView, CancelledView, stripe_webhook

urlpatterns = [
    path('config/', StripeConfigView.as_view(), name="stripe-config"),
    path('checkout/', CheckoutRender.as_view()),
    path('checkout-session/', StripeSessionView.as_view()),
    path('success/', SuccessView.as_view()),
    path('cancel/', CancelledView.as_view()),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook')
]
