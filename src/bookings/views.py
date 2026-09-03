from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bookings.models import Room, Booking
from decimal import Decimal, InvalidOperation
from datetime import datetime


@csrf_exempt
def create_room(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST request are allowed"},status=405)

    try:
        room_description = request.POST.get('room_description')
        price_room_raw = request.POST.get("price_room")

        if not room_description:
            return JsonResponse({"error": "room_description is not defind"},status=400)


        if not price_room_raw:
            return JsonResponse({"error": "price_room is not defind"},status=400)

        try:
            price_room = Decimal(price_room_raw)

        except InvalidOperation:
            return JsonResponse({"error": "price_room must be a valid decimal number"}, status=400)

        if price_room <= 0:
                        return JsonResponse({"error": "price_room must be greater than 0"}, status=400)

        room = Room.objects.create(
            room_description=room_description,
            price_room=price_room)

        return JsonResponse({"room_id": room.id}, status=201)
    
    except Exception as e:
        return JsonResponse({"error": f"Internal server error: {str(e)}"},status=500)


@csrf_exempt
def delete_room(request):
    if request.method != "POST":
            return JsonResponse({"error": "Only POST request are allowed"},status=405)
    
    room_id = request.POST.get('room_id')
    room = Room.objects.filter(id=room_id).first()
    if not room:
        return JsonResponse({"error": "Room not found"}, status=404)
    try:
        room.delete()
        return JsonResponse({"status": "success"}, status=200)

    except Exception as e:
        return JsonResponse({"error": f"Internal server error: {str(e)}"}, status=500)


@csrf_exempt
def list_room(request):
    if request.method != "GET":
        return JsonResponse({"error": "Only GET request are allowed"},status=405)

    allowed_fields = ['price_room', 'created_at']

    sort_by = request.GET.get('sort_by', 'created_at')
    order = request.GET.get('order', 'asc')

    if sort_by not in allowed_fields:
        sort_by = 'created_at'

    if order == 'desc':
        ordering_fields = f'-{sort_by}'
    else:
        ordering_fields = sort_by

    rooms = Room.objects.all().order_by(ordering_fields)

    rooms_data = [
    {
        "room_id": room.id,
        "room_description": room.room_description,
        "price_room": str(room.price_room)
    } 
    for room in rooms
    ]

    return JsonResponse(rooms_data, safe=False, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def create_booking(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

    try:
        room_id = request.POST.get("room")
        date_start_raw = request.POST.get("start_booking")
        date_end_raw = request.POST.get("end_booking")

        if not room_id:
            return JsonResponse({"error": "room is required"}, status=400)
        if not date_start_raw:
            return JsonResponse({"error": "start_booking is required"}, status=400)
        if not date_end_raw:
            return JsonResponse({"error": "end_booking is required"}, status=400)

        room = Room.objects.filter(id=room_id).first()
        if not room:
            return JsonResponse({"error": "Room not found"}, status=404)

        try:
            date_start = datetime.strptime(date_start_raw, "%Y-%m-%d").date()
            date_end = datetime.strptime(date_end_raw, "%Y-%m-%d").date()
        except ValueError:
            return JsonResponse({"error": "Dates must be in YYYY-MM-DD format and be valid"}, status=400)

        if date_start > date_end:
            return JsonResponse({"error": "start_booking cannot be after end_booking"}, status=400)

        overlapping_bookings = Booking.objects.filter(
            room=room,
            start_booking__lt=date_end,
            end_booking__gt=date_start
        ).exists()

        if overlapping_bookings:
            return JsonResponse({"error": "Room is already booked for these dates"}, status=400)

        booking = Booking.objects.create(
            room_id=room_id, # Передаем чистую цифру-строку из POST-запроса
            start_booking=date_start,
            end_booking=date_end
        )


        return JsonResponse({"booking_id": booking.id}, status=201)

    except Exception as e:
        return JsonResponse({"error": f"Internal server error: {str(e)}"}, status=500)


@csrf_exempt
def delete_booking(request):
    if request.method != "POST":
            return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

    booking_id = request.POST.get('booking_id')
    booking = Booking.objects.filter(id=booking_id).first()
    if not booking:
        return JsonResponse({"error": "Booking not found"}, status=404)
    try:
        booking.delete()
        return JsonResponse({"status": "success"}, status=200)
    
    except Exception as e:
        return JsonResponse({"error": f"Internal server error: {str(e)}"}, status=500)


@csrf_exempt
def list_bookings(request):
    if request.method != "GET":
        return JsonResponse({"error": "Only GET requests are allowed"}, status=405)

    room_id = request.GET.get('room_id')
    if not room_id:
        return JsonResponse({"error":"Room not found"}, status=400)

    bookings = Booking.objects.filter(room_id=room_id).order_by('start_booking')

    bookings_data = [
        {
            "booking_id": booking.id,
            "date_start": booking.start_booking.strftime("%Y-%m-%d"),
            "date_end": booking.end_booking.strftime("%Y-%m-%d"),
        } 
        for booking in bookings
    ]


    return JsonResponse(bookings_data, safe=False, json_dumps_params={'ensure_ascii': False})
    