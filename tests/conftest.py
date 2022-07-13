import pytest
from accounts.models import User
from cars.models import Car, Brand, Type
from rest_framework.test import APIClient


@pytest.fixture()
def user():
    user = User.objects.create_user(email="azhar.inexture@gmail.com",
                                    phone_number="+919987654329",
                                    password="Testing@321",
                                    password2="Testing@321"
                                   )
    return user


@pytest.fixture()
def superuser():
    user = User.objects.create_superuser(email="azhar.ajmeri@gmail.com",
                                         phone_number="+919987654328",
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
def auth_superuser_client(superuser, client):
    payload = {
        "email": "azhar.ajmeri@gmail.com",
        "password": "Testing@321",
    }
    response = client.post("/auth/login/", payload)
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    return client

@pytest.fixture
def auth_user_client(user, client):
    payload = {
        "email": "azhar.inexture@gmail.com",
        "password": "Testing@321",
    }
    response = client.post("/auth/login/", payload)
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    return client


@pytest.fixture()
def car():
    brand = Brand.objects.create(name="Tata", available=True)
    car_type = Type.objects.create(name="SUV", available=True)
    payload = {
        "name": "Nexon",
        "price": 2000,
        "reg_number": "GJ-01 EZ 5939",
        "brand": brand,
        "type": car_type,
        "available": True,
    }
    car = Car.objects.create(**payload)
    return car
