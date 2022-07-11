from django.urls import path
from .views import (
    CreateOrder,
    CancelOrder,
    ReturnCarOrder, 
    ViewBookings,
    ViewBookingHistory,
)

urlpatterns = [
    path('create/', CreateOrder.as_view(), name="create-booking"),
    path('<int:pk>/cancel/', CancelOrder.as_view(), name="cancel-booking"),
    path('<int:pk>/return-car/', ReturnCarOrder.as_view(), name="return-car"),

    path('bookings/', ViewBookings.as_view(), name="new-bookings"),
    path('bookings-history/', ViewBookingHistory.as_view(), name="booking-history"),
]
