from django.urls import path
from .views import *

app_name = 'boards'
urlpatterns = [
    path('find', FindRoomView.as_view(), name='find'),
    path('game/<int:room_id>', GameRoomView.as_view(), name='game'),
    path('create_room', CreateRoomView.as_view(), name='create_room'),
    path('create_board/<int:room_id>', NewBoardView.as_view(), name='create_board'),
]
