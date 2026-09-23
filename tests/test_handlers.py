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


@pytest.mark.django_db
def test_booking_zero_nights_fails(client):
    url = '/bookings/create'
    room = Room.objects.create(room_description="Стандарт", price_room="3000.00")
    data = {
        "room": room.id,
        "start_booking": "2026-11-01",
        "end_booking": "2026-11-01"
    }
    response = client.post(url, data=data)
    assert response.status_code == 400
    assert "error" in response.json()


@pytest.mark.django_db
def test_booking_overlapping_dates_fails(client):
    url = '/bookings/create'
    room = Room.objects.create(room_description="Стандарт", price_room="3000.00")
    Booking.objects.create(
        room=room,
        start_booking="2026-11-05",
        end_booking="2026-11-10"
    )
    data = {
        "room": room.id,
        "start_booking": "2026-11-07",
        "end_booking": "2026-11-09"
    }
    response = client.post(url, data=data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_booking_room_not_found(client):
    url = '/bookings/create'
    data = {
        "room": 99999,
        "start_booking": "2026-11-01",
        "end_booking": "2026-11-05"
    }
    response = client.post(url, data=data)
    assert response.status_code == 404


@pytest.mark.django_db
def test_create_room_invalid_price_fails(client):
    url = '/rooms/create'
    response = client.post(url, data={"room_description": "Тест", "price_room": "-100"})
    assert response.status_code == 400
    response = client.post(url, data={"room_description": "Тест", "price_room": "дорого"})
    assert response.status_code == 400


@pytest.mark.django_db
def test_delete_room_success(client):
    room = Room.objects.create(room_description="Люкс", price_room="5000.00")
    booking = Booking.objects.create(room=room, start_booking="2026-12-01", end_booking="2026-12-05")
    response = client.post('/rooms/delete', data={"room_id": room.id})
    assert response.status_code == 200
    assert not Room.objects.filter(id=room.id).exists()
    assert not Booking.objects.filter(id=booking.id).exists()


@pytest.mark.django_db
def test_get_rooms_list_sorting(client):
    Room.objects.create(room_description="Дешевая", price_room="1000.00")
    Room.objects.create(room_description="Дорогая", price_room="9000.00")
    response = client.get('/rooms/list?sort_by=price_room&order=desc')
    assert response.status_code == 200
    rooms_json = response.json()
    assert len(rooms_json) == 2
    assert rooms_json[0]["room_description"] == "Дорогая"


@pytest.mark.django_db
def test_get_bookings_list_for_room(client):
    room = Room.objects.create(room_description="Стандарт", price_room="2500.00")
    Booking.objects.create(room=room, start_booking="2026-10-01", end_booking="2026-10-05")
    response = client.get(f'/bookings/list?room_id={room.id}')
    assert response.status_code == 200
    bookings_json = response.json()
    assert len(bookings_json) == 1
    assert bookings_json[0]["date_start"] == "2026-10-01" or bookings_json[0].get("start_booking") == "2026-10-01"
