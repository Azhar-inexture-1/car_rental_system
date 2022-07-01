import pytest
from accounts.models import User
from rest_framework.test import APIClient


@pytest.fixture()
def user():
    user = User.objects.create_superuser(email="azhar.inexture@gmail.com",
                                         phone_number="+919987654329",
                                         password="Testing@321",
                                         password2="Testing@321"
                                         )
    return user


@pytest.fixture()
def client():
    client = APIClient()
    return client


@pytest.fixture
def refresh_token(user, client):
    payload = {
        "email": "azhar.inexture@gmail.com",
        "password": "Testing@321",
    }
    response = client.post("/auth/login/", payload)
    return response.data['refresh']


@pytest.fixture
def auth_client(user, client):
    payload = {
        "email": "azhar.inexture@gmail.com",
        "password": "Testing@321",
    }
    response = client.post("/auth/login/", payload)
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    return client
