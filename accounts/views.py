from rest_framework.response import Response

from rest_framework.generics import (
    CreateAPIView,
)

from rest_framework.permissions import (
    IsAuthenticated,
)

from .models import (
    User
)

from .serializers import (
    UserRegistrationSerializer
)


class UserRegistrationAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


user_registration_view = UserRegistrationAPIView.as_view()
