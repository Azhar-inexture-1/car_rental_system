from rest_framework import serializers
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer class for registration of new users
    """

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError({
                "password": "password don't match.",
                "password2": "password don't match.",
            })
        return attrs

    def create(self, validate_data):
        """calling the create user method from models
        """
        return User.objects.create_user(**validate_data)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer class for profile of users
    """

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number']
