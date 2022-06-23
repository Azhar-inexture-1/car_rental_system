from django.urls import path
from .views import (
    CreateOrder
)

urlpatterns = [
    path('create/', CreateOrder.as_view())
]
