from django.urls import path
from .views import (
    user_registration_view
)

urlpatterns = [
    path('register/', user_registration_view, name='user-register')
]
