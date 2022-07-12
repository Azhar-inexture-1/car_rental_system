import pytest
from cars.models import Brand, Type


@pytest.mark.django_db
def test_create_car_brand_success(auth_client):
    payload = {
        "name": "Tata",
        "available": True,
    }
    response = auth_client.post("/cars/list_create_brand/", payload)
    data = response.data
    assert response.status_code == 201
    assert data["name"] == payload["name"]
    assert data["available"] == payload["available"]


@pytest.mark.django_db
def test_create_car_brand_fail(auth_client):
    payload = {}
    response = auth_client.post("/cars/list_create_brand/", payload)
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_car_type_success(auth_client):
    payload = {
        "name": "SUV",
        "available": True,
    }
    response = auth_client.post("/cars/list_create_type/", payload)
    data = response.data
    assert response.status_code == 201
    assert data["name"] == payload["name"]
    assert data["available"] == payload["available"]


@pytest.mark.django_db
def test_create_car_type_fail(auth_client):
    payload = {}
    response = auth_client.post("/cars/list_create_type/", payload)
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_car_success(auth_client):
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
    response = auth_client.post("/cars/list_create_car/", payload)
    data = response.data
    assert response.status_code == 201
    assert data["name"] == payload["name"]
    assert data["brand"] == payload["brand"]
    assert data["type"] == payload["type"]
    assert data["available"] == payload["available"]
    assert data["reg_number"] == payload["reg_number"]


@pytest.mark.django_db
def test_create_car_fail(auth_client):
    brand = Brand.objects.create(name="Tata", available=True)
    car_type = Type.objects.create(name="SUV", available=True)
    payload = {
        "price": 2000,
        "reg_number": "GJ-01 EZ 5939",
        "brand": brand.id,
        "type": car_type.id,
        "available": True,
    }
    response = auth_client.post("/cars/list_create_car/", payload)
    assert response.status_code == 400


@pytest.mark.django_db
def test_list_car_fail_0(auth_client):
    response = auth_client.get("/cars/list_create_car/?start_date=2022-6-7&end_date=2022-6-7")
    assert response.status_code == 400
    assert response.data['message'] == "Invalid request, start date should be today or later."


@pytest.mark.django_db
def test_list_car_fail_1(auth_client):
    response = auth_client.get("/cars/list_create_car/?start_date=2022-7-14&end_date=2022-7-12")
    assert response.status_code == 400
    assert response.data['message'] == "Invalid request, start date should be before the end date."


@pytest.mark.django_db
def test_list_car_success(auth_client):
    response = auth_client.get("/cars/list_create_car/?start_date=2022-7-14&end_date=2022-7-16")
    assert response.status_code == 200
