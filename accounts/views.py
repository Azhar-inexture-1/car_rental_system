from rest_framework.generics import (
    CreateAPIView,
)

from .models import (
    User
)

from .serializers import (
    UserRegistrationSerializer
)


class UserRegistrationAPIView(CreateAPIView):
    """Create View for registration of new users"""

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


user_registration_view = UserRegistrationAPIView.as_view()
