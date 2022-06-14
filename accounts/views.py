from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,

)
from django_rest_passwordreset.views import ResetPasswordConfirm, ResetPasswordRequestToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer
)
from .permissions import IsOwner


class UserRegistrationAPIView(CreateAPIView):
    """Create View for registration of new users"""

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        response = super(UserRegistrationAPIView, self).post(request, *args, **kwargs)
        return Response(
            {"data": response.data, "message": "User registered successfully."},
            status=response.status_code
        )


class UserProfileAPIView(RetrieveUpdateDestroyAPIView):
    """Retrieve, Update and Destroy View for users model"""

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def patch(self, request, *args, **kwargs):
        response = super(UserProfileAPIView, self).partial_update(request, *args, **kwargs)
        return Response(
            {"data": response.data, "message": "Profile updated successfully."},
            status=response.status_code
        )

    def delete(self, request, *args, **kwargs):
        response = super(UserProfileAPIView, self).destroy(request, *args, **kwargs)
        return Response(
            {"data": response.data, "message": "Profile deleted successfully."},
            status=response.status_code
        )


class PasswordResetView(ResetPasswordRequestToken):
    """Overriding post method for changing Response"""

    def post(self, request, *args, **kwargs):
        response = super(PasswordResetView, self).post(request)
        return Response(
            {'status': 'OK', 'message': 'Password reset link sent.'},
            status=response.status_code
        )


class PasswordResetConfirm(ResetPasswordConfirm):
    """Overriding post method for changing Response"""

    def post(self, request, *args, **kwargs):
        response = super(PasswordResetConfirm, self).post(request)
        return Response(
            {'status': 'OK', 'message': 'Password successfully reset.'},
            status=response.status_code
        )
