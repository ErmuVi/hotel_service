from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bookings.models import Room
from decimal import Decimal, InvalidOperation


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

