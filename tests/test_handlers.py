import pytest
from django.urls import reverse
from bookings.models import Room, Booking

@pytest.mark.django_db
def test_create_room_success(client):
    url = '/rooms/create' 
    
    data = {
        "room_description": "Тестовый шикарный люкс",
        "price_room": "6500.00"
    }
    response = client.post(url, data=data)
    
    assert response.status_code == 201
    
    response_json = response.json()
    assert "room_id" in response_json
    
    assert Room.objects.filter(id=response_json["room_id"]).exists()


@pytest.mark.django_db
def test_booking_success(client):
    url = '/bookings/create'

    room = Room.objects.create(
        room_description="Тестовый шикарный люкс", 
        price_room="6500.00"
    )

    data = {
        "room": room.id, 
        "start_booking": "2026-10-01",
        "end_booking": "2026-10-05"
    }

    response = client.post(url, data=data)

    assert response.status_code == 201
    assert "booking_id" in response.json()

