import pytest
from accounts.models import User
from cars.models import Car, Brand, Type
from orders.models import Order
from rest_framework.test import APIClient
from datetime import datetime, timedelta


@pytest.fixture()
def user():
    """Customer user fixture for testing purpose.
    """
    user = User.objects.create_user(email="azhar.inexture@gmail.com",
                                    phone_number="+919987654329",
                                    password="Testing@321",
                                    password2="Testing@321"
                                   )
    return user


@pytest.fixture()
def superuser():
    """Admin user fixture for testing purpose.
    """
    user = User.objects.create_superuser(email="azhar.ajmeri@gmail.com",
                                         phone_number="+919987654328",
                                         password="Testing@321",
                                         password2="Testing@321"
                                        )
    return user


@pytest.fixture()
def client():
    """API client without access credentails.
        Used for accessing the endpoints of the project.
    """
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
    """API client with access credentails of Admin user.
        Used for accessing the endpoints of the project.
    """
    payload = {
        "email": "azhar.ajmeri@gmail.com",
        "password": "Testing@321",
    }
    response = client.post("/auth/login/", payload)
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    return client

@pytest.fixture
def auth_user_client(user, client):
    """API client with access credentails of customer user.
        Used for accessing the endpoints of the project.
    """
    payload = {
        "email": "azhar.inexture@gmail.com",
        "password": "Testing@321",
    }
    response = client.post("/auth/login/", payload)
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    return client


@pytest.fixture()
def car():
    """ :model:`cars.Car` fixture for testing endpoints.
    """
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


@pytest.fixture()
def order(car, user):
    """ :model:`orders.Order` fixture for testing endpoints.
    """
    date = (datetime.today() + timedelta(days=2)).strftime('%Y-%m-%d')
    payload = {
        "user": user,
        "car": car,
        "start_date": date,
        "end_date": date,
        "price": 1000,
        "discount": 0,
        "payment_intent_id": 'abc',
        "fine_payment_intent_id": 'abc',
    }
    order = Order.objects.create(**payload)
    return order


@pytest.fixture()
def order_today(car, user):
    """ :model:`orders.Order` fixture for testing endpoints.
        The objects has booking dates of today.
    """
    date = datetime.today().strftime('%Y-%m-%d')
    payload = {
        "user": user,
        "car": car,
        "start_date": date,
        "end_date": date,
        "price": 1000,
        "discount": 0,
        "payment_intent_id": 'abc',
        "fine_payment_intent_id": 'abc',
    }
    order = Order.objects.create(**payload)
    return order


@pytest.fixture()
def order_return_late(car, user):
    """ :model:`orders.Order` fixture for testing endpoints.
        The objects has booking dates are set in away which generated
        fine when order is returned.
    """
    date = (datetime.today() - timedelta(days=4)).strftime('%Y-%m-%d')
    payload = {
        "user": user,
        "car": car,
        "start_date": date,
        "end_date": date,
        "price": 1000,
        "discount": 0,
        "payment_intent_id": 'abc',
        "fine_payment_intent_id": 'abc',
    }
    order = Order.objects.create(**payload)
    return order


@pytest.fixture()
def order_early(car, user):
    """ :model:`orders.Order` fixture for testing endpoints.
        The objects has booking dates are set in away which doesn't
        allow user to return the car because of invalid dates.

        User can only return a car which has order dates of today or before.
    """
    date = (datetime.today() + timedelta(days=4)).strftime('%Y-%m-%d')
    payload = {
        "user": user,
        "car": car,
        "start_date": date,
        "end_date": date,
        "price": 1000,
        "discount": 0,
        "payment_intent_id": 'abc',
        "fine_payment_intent_id": 'abc',
    }
    order = Order.objects.create(**payload)
    return order