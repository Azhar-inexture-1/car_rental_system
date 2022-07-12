import pytest


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
def test_get_profile(auth_client):
    response = auth_client.get("/auth/profile/")
    data = response.data
    assert response.status_code == 200
    assert data["email"] == "azhar.inexture@gmail.com"
    assert data["first_name"] == ""
    assert data["last_name"] == ""
    assert data["phone_number"] == "+919987654329"


@pytest.mark.django_db
def test_get_profile(auth_client):
    payload = {
        "phone_number": "+919987654320",
        "first_name": "Azhar",
        "last_name": "Ajmeri",
    }
    response = auth_client.patch("/auth/profile/", payload)
    data = response.data["data"]
    assert response.status_code == 200
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert data["phone_number"] == payload["phone_number"]
