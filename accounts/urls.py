from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    UserRegistrationAPIView,
    UserProfileAPIView,
    PasswordResetView,
    PasswordResetConfirm,
)

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # password reset url from the django_rest_passwordreset package
    path('password_reset/confirm/', PasswordResetConfirm.as_view(), name="password-reset-confirm"),
    path('password_reset/', PasswordResetView.as_view(), name="password-reset"),

    # profile Retrieve, Update, Destroy URL
    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),
]
