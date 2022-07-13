import pytest
from constants import INVALID_START_END_DATE, INVALID_START_DATE, PROVIDE_START_END_DATE

@pytest.mark.django_db
def test_create_order_success(car, auth_user_client):
    payload = {
        "car": car.id,
        "start_date": '2022-07-13',
        "end_date": '2022-07-13',
    }
    response = auth_user_client.post('/payments/checkout-session/', payload)
    assert response.status_code == 200
    assert "sessionId" in response.data


@pytest.mark.django_db
def test_create_order_fail_INVALID_START_DATE(car, auth_user_client):
    payload = {
        "car": car.id,
        "start_date": '2022-07-12',
        "end_date": '2022-07-13',
    }
    response = auth_user_client.post('/payments/checkout-session/', payload)
    assert response.status_code == 400
    assert response.data['message'] == INVALID_START_DATE


@pytest.mark.django_db
def test_create_order_fail_INVALID_START_END_DATE(car, auth_user_client):
    payload = {
        "car": car.id,
        "start_date": '2022-07-15',
        "end_date": '2022-07-13',
    }
    response = auth_user_client.post('/payments/checkout-session/', payload)
    assert response.status_code == 400
    assert response.data['message'] == INVALID_START_END_DATE


@pytest.mark.django_db
def test_create_order_fail_PROVIDE_START_END_DATE(car, auth_user_client):
    payload = {
        "car": car.id
    }
    response = auth_user_client.post('/payments/checkout-session/', payload)
    assert response.status_code == 400
    assert response.data['message'] == PROVIDE_START_END_DATE



@pytest.mark.django_db
def test_cancel_order_success(order, auth_user_client):
    
    response = auth_user_client.post(f'/orders/{}/cancel/')
    assert response.status_code == 200
    assert "sessionId" in response.data
