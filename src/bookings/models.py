from django.db import models


class Room(models.Model):    
    """Hotel room"""
    room_description = models.TextField()
    price_room = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    start_booking = models.DateField()
    end_booking = models.DateField()
