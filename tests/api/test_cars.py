import pytest
from cars.models import Brand, Type, Car
from constants import INVALID_START_DATE, INVALID_START_END_DATE, DELETE_SUCCESS


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
    response = auth_user_client.get("/cars/list_create_car/?start_date=2022-7-14&end_date=2022-7-16")
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
    