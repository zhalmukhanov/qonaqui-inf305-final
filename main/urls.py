from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),

    path('dashboard/', dashboard, name='dashboard'),

    path('registration/', registration, name='registration'),
    path('registration/room/<int:pk>', registration_room, name='registration_room'),
    path('add_client/<int:pk>', add_client, name='add_client'),
    path('add_search_client/<int:pk>/<int:id>', add_search_client, name='add_search_client'),

    path('rooms/', rooms, name='rooms'),
    path('room_page/<int:pk>', room_page, name='room_page'),
    path('remove_room/<int:pk>', remove_room, name='remove_room'),
    path('add_room/', add_room, name='add_room'),

    path('clients/', clients, name='clients'),

    path('payment/', payment, name='payment'),
    path('payment/room/<int:pk>', payment_room, name='payment_room'),
    path('pay/<int:pk>', pay, name='pay'),

    path('history/', history, name='history'),

]