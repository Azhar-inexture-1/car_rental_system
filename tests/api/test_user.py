import pytest
from constants import DELETE_USER_PROFILE_SUCCESS, DELETE_USER_EXISTING_BOOKINGS
from cars.models import Brand, Type, Car
from orders.models import Order


@pytest.mark.django_db
def test_register_user_fail(client):
    payload = {
        "email": "azhar.inexture@gmail.com",
        "phone_number": "+919987654329",
        "password": "testing@321",
        "password2": "testing@321",
    }
    response = client.post("/auth/register/", payload)
    data = response.data
    assert response.status_code == 400
    assert data['password'][0] == "The password must contain at least 1 uppercase letter, A-Z."


@pytest.mark.django_db
def test_register_user_success(client):
    payload = {
        "email": "azhar.inexture@gmail.com",
        "phone_number": "+919987654329",
        "password": "Testing@321",
        "password2": "Testing@321",
    }
    response = client.post("/auth/register/", payload)
    data = response.data
    assert response.status_code == 201
    assert data["data"]["email"] == payload["email"]
    assert data["data"]["phone_number"] == payload["phone_number"]
    assert "password" not in data["data"]
    assert "password2" not in data["data"]

    login_payload = {
        "email": "azhar.inexture@gmail.com",
        "password": "Testing@321",
    }
    response = client.post("/auth/login/", login_payload)
    data = response.data
    assert response.status_code == 200
    assert "access" in data
    assert "refresh" in data


@pytest.mark.django_db
def test_user_login_fail(user, client):
    payload = {
        "email": "new.inexture@gmail.com",
        "password": "Hacking@321",
    }
    response = client.post("/auth/login/", payload)
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_login_success(user, client):
    payload = {
        "email": "azhar.inexture@gmail.com",
        "password": "Testing@321",
    }
    response = client.post("/auth/login/", payload)
    assert response.status_code == 200


@pytest.mark.django_db
def test_token_refresh(client, refresh_token):
    response = client.post("/auth/token/refresh/", {'refresh': refresh_token})
    data = response.data
    assert response.status_code == 200
    assert "access" in data


@pytest.mark.django_db
def test_get_profile(auth_user_client):
    response = auth_user_client.get("/auth/profile/")
    data = response.data
    assert response.status_code == 200
    assert data["email"] == "azhar.inexture@gmail.com"
    assert data["first_name"] == ""
    assert data["last_name"] == ""
    assert data["phone_number"] == "+919987654329"


@pytest.mark.django_db
def test_update_profile_success(auth_user_client):
    payload = {
        "phone_number": "+919987654320",
        "first_name": "Azhar",
        "last_name": "Ajmeri",
    }
    response = auth_user_client.patch("/auth/profile/", payload)
    data = response.data["data"]
    assert response.status_code == 200
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert data["phone_number"] == payload["phone_number"]


@pytest.mark.django_db
def test_update_profile_fail(auth_user_client):
    payload = {
        "phone_number": "9987654320",
        "first_name": "Azhar",
        "last_name": "Ajmeri",
    }
    response = auth_user_client.patch("/auth/profile/", payload)
    data = response.data
    assert response.status_code == 400
    assert data['phone_number'][0] == "The phone number entered is not valid."


@pytest.mark.django_db
def test_delete_profile_fail(client):
    response = client.delete("/auth/profile/")
    data = response.data
    assert response.status_code == 401
    assert data['detail'] == 'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_delete_profile_fail_for_existing_order(user, auth_user_client):
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
    payload = {
        "user": user,
        "car": car,
        "start_date": '2022-07-13',
        "end_date": '2022-07-13',
        "price": 1000,
        "discount": 0,
        "payment_intent_id": 'abc',
        "fine_payment_intent_id": 'abc',
    }
    Order.objects.create(**payload)
    response = auth_user_client.delete("/auth/profile/")
    data = response.data
    assert response.status_code == 400
    assert data['message'] == DELETE_USER_EXISTING_BOOKINGS


@pytest.mark.django_db
def test_delete_profile_success(auth_user_client):
    response = auth_user_client.delete("/auth/profile/")
    data = response.data
    assert response.status_code == 204
    assert data['message'] == DELETE_USER_PROFILE_SUCCESS
