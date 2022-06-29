from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from django_rest_passwordreset.views import ResetPasswordConfirm, ResetPasswordRequestToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from orders.models import Order
from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer
)
from .permissions import IsOwner
from constants import (
    REGISTRATION_SUCCESS,
    PROFILE_UPDATE_SUCCESS,
    DELETE_USER_EXISTING_BOOKINGS,
    DELETE_USER_PROFILE_SUCCESS,
    PASSWORD_RESET_LINK_SENT,
    PASSWORD_RESET_SUCCESS,
)


class UserRegistrationAPIView(CreateAPIView):
    """Create View for registration of new users"""

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        response = super(UserRegistrationAPIView, self).post(request, *args, **kwargs)
        return Response(
            {"data": response.data, "message": REGISTRATION_SUCCESS},
            status=response.status_code
        )


class UserProfileAPIView(RetrieveUpdateDestroyAPIView):
    """Retrieve, Update and Destroy View for users model"""

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj

    def patch(self, request, *args, **kwargs):
        response = super(UserProfileAPIView, self).partial_update(request, *args, **kwargs)
        return Response(
            {"data": response.data, "message": PROFILE_UPDATE_SUCCESS},
            status=response.status_code
        )

    def delete(self, request, *args, **kwargs):
        if Order.objects.filter(returned=False, user=self.get_object()).exists():
            return Response(
                {"status": "OK", "message": DELETE_USER_EXISTING_BOOKINGS},
                status=status.HTTP_400_BAD_REQUEST
            )
        response = super(UserProfileAPIView, self).destroy(request, *args, **kwargs)
        return Response(
            {"data": response.data, "message": DELETE_USER_PROFILE_SUCCESS},
            status=response.status_code
        )


class PasswordResetView(ResetPasswordRequestToken):
    """Overriding post method for changing Response"""

    def post(self, request, *args, **kwargs):
        response = super(PasswordResetView, self).post(request)
        return Response(
            {'status': 'OK', 'message': PASSWORD_RESET_LINK_SENT},
            status=response.status_code
        )


class PasswordResetConfirm(ResetPasswordConfirm):
    """Overriding post method for changing Response"""

    def post(self, request, *args, **kwargs):
        response = super(PasswordResetConfirm, self).post(request)
        return Response(
            {'status': 'OK', 'message': PASSWORD_RESET_SUCCESS},
            status=response.status_code
        )
