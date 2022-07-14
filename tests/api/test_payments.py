import pytest
from datetime import datetime
from constants import INVALID_START_DATE, INVALID_START_END_DATE, PROVIDE_START_END_DATE

def test_StripeConfigView_success(client):
    response = client.get('/payments/config/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_session_success(car, auth_user_client):
    date = datetime.today().strftime('%Y-%m-%d')
    payload = {
        "car": car.id,
        "start_date": date,
        "end_date": date,
    }
    response = auth_user_client.post('/payments/checkout-session/', payload)
    assert response.status_code == 200
    assert "sessionId" in response.data

@pytest.mark.django_db
def test_create_session_fail_INVALID_START_DATE(car, auth_user_client):
    """Fetching the car list for given dates fails.
        The dates should be of today or later.
        User cannot book cars for those given dates in url.
    """
    payload = {
        "car": car.id,
        "start_date": '2022-07-12',
        "end_date": '2022-07-13',
    }
    response = auth_user_client.post('/payments/checkout-session/', payload)
    assert response.status_code == 400
    assert response.data['message'] == INVALID_START_DATE


@pytest.mark.django_db
def test_create_session_fail_INVALID_START_END_DATE(car, auth_user_client):
    """Fetching the car list for given dates fails.
        The start date should be before the end date.
        Example
        -------
            start-date: 2022-06-06
            end-date: 2022-06-14
        
        The dates should be of today or later.
        User cannot book cars for those currently given dates in the url.
    """
    payload = {
        "car": car.id,
        "start_date": '2022-07-15',
        "end_date": '2022-07-13',
    }
    response = auth_user_client.post('/payments/checkout-session/', payload)
    assert response.status_code == 400
    assert response.data['message'] == INVALID_START_END_DATE


@pytest.mark.django_db
def test_create_session_fail_PROVIDE_START_END_DATE(car, auth_user_client):
    """The start date and end date are mandatory for booking a car.
        Example
        -------
            start-date: 2022-06-06
            end-date: 2022-06-14
        
        The dates should be of today or later.
    """
    payload = {
        "car": car.id
    }
    response = auth_user_client.post('/payments/checkout-session/', payload)
    assert response.status_code == 400
    assert response.data['message'] == PROVIDE_START_END_DATE


@pytest.mark.django_db
def test_create_fine_session_fail(order, auth_user_client):
    """User cannot create a payment session for a order which has no fine.
    """
    order.fine_paid = False
    order.fine_generated = False
    order.save()
    response = auth_user_client.post(f'/payments/{order.id}/fine-checkout-session/')
    assert response.status_code == 400
    assert response.data["message"] == "Invalid request, no fine generated on this order."


@pytest.mark.django_db
def test_create_fine_session_fail_already_paid(order, auth_user_client):
    """User cannot create a payment session for a order which has fine
        and is already been paid.
    """
    order.fine_generated = True
    order.fine_paid = True
    order.save()
    response = auth_user_client.post(f'/payments/{order.id}/fine-checkout-session/')
    assert response.status_code == 400
    assert response.data["message"] == "Invalid request, fine amount already paid."


@pytest.mark.django_db
def test_create_fine_session_success(order, auth_user_client):
    order.fine_generated = True
    order.fine_paid = False
    order.fine_amount = 1000
    order.save()
    response = auth_user_client.post(f'/payments/{order.id}/fine-checkout-session/')
    assert response.status_code == 200



@pytest.mark.django_db
def test_discount_create_success(auth_superuser_client):
    payload = {
        "name": "DISCOUNT10",
        "percentage_off": 10
    }
    response = auth_superuser_client.post('/payments/create-discount-coupon/', payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_discount_delete_success(auth_superuser_client):
    payload = {
        "name": "DISCOUNT10",
        "percentage_off": 10
    }
    response = auth_superuser_client.post('/payments/create-discount-coupon/', payload)
    assert response.status_code == 201

    response = auth_superuser_client.delete(f'/payments/{response.data["id"]}/delete-discount-coupon/')
    assert response.status_code == 204