from django.urls import path
from bookings.views import create_room, delete_room, list_room

urlpatterns = [
    path('create', create_room, name='create_room'),
    path('delete', delete_room, name='delete_room'),
    path('list', list_room, name='list_room'),
]
