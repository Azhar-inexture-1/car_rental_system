import pytest
from cars.models import Brand, Type, Car
from constants import (
    DELETE_TYPE_EXISTING_BOOKINGS,
    INVALID_START_DATE,
    INVALID_START_END_DATE,
    DELETE_SUCCESS,
    DELETE_BRAND_EXISTING_BOOKINGS,
    DELETE_CAR_EXISTING_BOOKINGS
)
from datetime import datetime
from orders.models import Order

@pytest.mark.django_db
def test_create_car_brand_success(auth_superuser_client):
    payload = {
        "name": "Tata",
        "available": True,
    }
    response = auth_superuser_client.post("/cars/list_create_brand/", payload)
    data = response.data
    assert response.status_code == 201
    assert data["name"] == payload["name"]
    assert data["available"] == payload["available"]

@pytest.mark.django_db
def test_update_brand_success(auth_superuser_client):
    brand = Brand.objects.create(name="T", available=True)
    payload = {
        "name": "Tata",
    }
    response = auth_superuser_client.patch(f"/cars/{brand.id}/brand_detail/", payload)
    assert response.status_code == 200
    assert response.data['data']["name"] == payload["name"]

@pytest.mark.django_db
def test_create_car_brand_fail_not_admin(auth_user_client):
    """The `auth_user_client` is not an admin user.
    """
    payload = {
        "name": "Tata",
        "available": True,
    }
    response = auth_user_client.post("/cars/list_create_brand/", payload)
    assert response.status_code == 403


@pytest.mark.django_db
def test_create_car_brand_fail(auth_superuser_client):
    """The payload is empty, required field are not provided.
    """
    payload = {}
    response = auth_superuser_client.post("/cars/list_create_brand/", payload)
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_car_type_success(auth_superuser_client):
    payload = {
        "name": "SUV",
        "available": True,
    }
    response = auth_superuser_client.post("/cars/list_create_type/", payload)
    data = response.data
    assert response.status_code == 201
    assert data["name"] == payload["name"]
    assert data["available"] == payload["available"]


@pytest.mark.django_db
def test_update_type_success(auth_superuser_client):
    type = Type.objects.create(name="SU", available=True)
    payload = {
        "name": "SUV",
    }
    response = auth_superuser_client.patch(f"/cars/{type.id}/type_detail/", payload)
    assert response.status_code == 200
    assert response.data['data']["name"] == payload["name"]


@pytest.mark.django_db
def test_create_car_type_fail_not_admin(auth_user_client):
    """The `auth_user_client` is not an admin user.
    """
    payload = {
        "name": "SUV",
        "available": True,
    }
    response = auth_user_client.post("/cars/list_create_type/", payload)
    assert response.status_code == 403


@pytest.mark.django_db
def test_create_car_type_fail(auth_superuser_client):
    """The payload is empty, required field are not provided.
    """
    payload = {}
    response = auth_superuser_client.post("/cars/list_create_type/", payload)
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_car_success(auth_superuser_client):
    brand = Brand.objects.create(name="Tata", available=True)
    car_type = Type.objects.create(name="SUV", available=True)
    payload = {
        "name": "Nexon",
        "price": 2000,
        "reg_number": "GJ-01 EZ 5939",
        "brand": brand.id,
        "type": car_type.id,
        "available": True,
    }
    response = auth_superuser_client.post("/cars/list_create_car/", payload)
    data = response.data
    assert response.status_code == 201
    assert data["name"] == payload["name"]
    assert data["brand"] == payload["brand"]
    assert data["type"] == payload["type"]
    assert data["available"] == payload["available"]
    assert data["reg_number"] == payload["reg_number"]


@pytest.mark.django_db
def test_create_car_fail_not_admin(auth_user_client):
    """The `auth_user_client` is not an admin user.
    """
    brand = Brand.objects.create(name="Tata", available=True)
    car_type = Type.objects.create(name="SUV", available=True)
    payload = {
        "name": "Nexon",
        "price": 2000,
        "reg_number": "GJ-01 EZ 5939",
        "brand": brand.id,
        "type": car_type.id,
        "available": True,
    }
    response = auth_user_client.post("/cars/list_create_car/", payload)
    assert response.status_code == 403

@pytest.mark.django_db
def test_create_car_fail(auth_superuser_client):
    """The payload is empty, required field are not provided.
        `car.name` is not provided in the payload.
    """
    brand = Brand.objects.create(name="Tata", available=True)
    car_type = Type.objects.create(name="SUV", available=True)
    payload = {
        "price": 2000,
        "reg_number": "GJ-01 EZ 5939",
        "brand": brand.id,
        "type": car_type.id,
        "available": True,
    }
    response = auth_superuser_client.post("/cars/list_create_car/", payload)
    assert response.status_code == 400


@pytest.mark.django_db
def test_list_car_fail_INVALID_START_DATE(auth_user_client):
    """Fetching the car list for given dates fails.
        The dates should be of today or later.
        User cannot book cars for those given dates in url.
    """
    response = auth_user_client.get("/cars/list_create_car/?start_date=2022-6-7&end_date=2022-6-7")
    assert response.status_code == 400
    assert response.data['message'] == INVALID_START_DATE


@pytest.mark.django_db
def test_list_car_fail_INVALID_START_END_DATE(auth_user_client):
    """Fetching the car list for given dates fails.
        The start date should be before the end date.
        Example
        -------
            start-date: 2022-06-06
            end-date: 2022-06-14
        
        The dates should be of today or later.
        User cannot book cars for those given dates currently given in the url.
    """
    response = auth_user_client.get("/cars/list_create_car/?start_date=2022-7-14&end_date=2022-7-12")
    assert response.status_code == 400
    assert response.data['message'] == INVALID_START_END_DATE


@pytest.mark.django_db
def test_list_car_success(auth_user_client):
    date = datetime.today().strftime('%Y-%m-%d')
    response = auth_user_client.get(f"/cars/list_create_car/?start_date={date}&end_date={date}")
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_car_success_without_dates(auth_user_client):
    response = auth_user_client.get("/cars/list_create_car/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_retrieve_car_fail(auth_user_client):
    """The given `car.id` is not present in the database.
        So it returns 404 not found.
    """
    response = auth_user_client.get("/cars/1/car_detail/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_retrieve_car_success(auth_user_client):
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
    response = auth_user_client.get(f"/cars/{car.id}/car_detail/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_car_success(auth_superuser_client):
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
        "name": "Nexon XL",
        "price": "3000.00",
        "reg_number": "GJ-01 EZ 0060"
    }
    response = auth_superuser_client.patch(f"/cars/{car.id}/car_detail/", payload)
    assert response.status_code == 200
    assert response.data['data']["name"] == payload["name"]
    assert response.data['data']["price"] == payload["price"]
    assert response.data['data']["reg_number"] == payload["reg_number"]


@pytest.mark.django_db
def test_update_car_fail(auth_user_client):
    """The `auth_user_client` doesn't have admin rights to perform the 
        update.
        The user must be an admin to perform this action.
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
    payload = {
        "name": "Nexon XL",
        "price": "3000.00",
        "reg_number": "GJ-01 EZ 0060"
    }
    response = auth_user_client.patch(f"/cars/{car.id}/car_detail/", payload)
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_car_success(auth_superuser_client):
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
    response = auth_superuser_client.delete(f"/cars/{car.id}/car_detail/", payload)
    assert response.status_code == 204
    assert response.data['message'] == DELETE_SUCCESS


@pytest.mark.django_db
def test_delete_brand_type_success(auth_superuser_client):
    brand = Brand.objects.create(name="Tata", available=True)
    car_type = Type.objects.create(name="SUV", available=True)
    response = auth_superuser_client.delete(f"/cars/{brand.id}/brand_detail/")
    assert response.status_code == 204
    assert response.data['message'] == DELETE_SUCCESS

    response = auth_superuser_client.delete(f"/cars/{car_type.id}/type_detail/")
    assert response.status_code == 204
    assert response.data['message'] == DELETE_SUCCESS


@pytest.mark.django_db
def test_delete_car_fail(auth_user_client):
    """The `auth_user_client` doesn't have admin rights to perform the 
        update.
        The user must be an admin to perform this action.
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
    response = auth_user_client.delete(f"/cars/{car.id}/car_detail/", payload)
    assert response.status_code == 403
    assert response.data['detail'] == "You do not have permission to perform this action."
    

@pytest.mark.django_db
def test_delete_car_type_brand_fail(auth_superuser_client, user):
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
    Order.objects.create(**payload)
    response = auth_superuser_client.delete(f"/cars/{car.id}/car_detail/", payload)
    assert response.status_code == 400
    assert response.data['message'] == DELETE_CAR_EXISTING_BOOKINGS


    response = auth_superuser_client.delete(f"/cars/{brand.id}/brand_detail/", payload)
    assert response.status_code == 400
    assert response.data['message'] == DELETE_BRAND_EXISTING_BOOKINGS


    response = auth_superuser_client.delete(f"/cars/{car_type.id}/type_detail/", payload)
    assert response.status_code == 400
    assert response.data['message'] == DELETE_TYPE_EXISTING_BOOKINGS
