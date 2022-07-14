import pytest
from constants import (
    INVALID_REQUEST,
    INVALID_START_END_DATE,
    INVALID_START_DATE,
    PROVIDE_START_END_DATE,
    CAR_RETURN_SUCCESS,
)
from datetime import datetime


@pytest.mark.django_db
def test_create_order_success(car, auth_user_client):
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
def test_create_order_fail_INVALID_START_DATE(car, auth_user_client):
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
def test_create_order_fail_INVALID_START_END_DATE(car, auth_user_client):
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
def test_create_order_fail_PROVIDE_START_END_DATE(car, auth_user_client):
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



# @pytest.mark.django_db
# def test_cancel_order_success(order, auth_user_client):
#     response = auth_user_client.post(f'/orders/{order.id}/cancel/')
#     assert response.status_code == 400


@pytest.mark.django_db
def test_return_order_success(order_today, auth_user_client):
    response = auth_user_client.post(f'/orders/{order_today.id}/return-car/')
    data = response.data["data"]
    assert response.status_code == 200
    assert data["fine_generated"] == False
    assert response.data["message"] == CAR_RETURN_SUCCESS


@pytest.mark.django_db
def test_return_order_late_success(order_return_late, auth_user_client):
    """When the user returns the car late, fine is generated.
    """
    response = auth_user_client.post(f'/orders/{order_return_late.id}/return-car/')
    data = response.data["data"]
    assert response.status_code == 200
    assert data["fine_generated"] == True
    assert response.data["message"] == CAR_RETURN_SUCCESS


@pytest.mark.django_db
def test_return_order_returned_fail(order, auth_user_client):
    """The user cannot resubmit the car which is already submitted.
    """
    order.returned = True
    order.save()
    response = auth_user_client.post(f'/orders/{order.id}/return-car/')
    assert response.status_code == 400
    assert response.data["message"] == INVALID_REQUEST


@pytest.mark.django_db
def test_return_order_cancelled_fail(order, auth_user_client):
    """The user cannot cancel the order which is already cancelled.
    """
    order.cancelled = True
    order.save()
    response = auth_user_client.post(f'/orders/{order.id}/return-car/')
    assert response.status_code == 400
    assert response.data["message"] == INVALID_REQUEST


@pytest.mark.django_db
def test_return_order_early_fail(order_early, auth_user_client):
    """If user tries to submit the car before the start_date,
        then he is refused.
    """
    order_early.cancelled = True
    order_early.save()
    response = auth_user_client.post(f'/orders/{order_early.id}/return-car/')
    assert response.status_code == 400
    assert response.data["message"] == INVALID_REQUEST


@pytest.mark.django_db
def test_view_bookings(auth_user_client):
    response = auth_user_client.get('/orders/bookings/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_bookings_history(auth_user_client):
    response = auth_user_client.get('/orders/bookings-history/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_bookings_fine(auth_user_client):
    response = auth_user_client.get('/orders/pending-fine/')
    assert response.status_code == 200
