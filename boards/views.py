from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .constants import *
from django.contrib.auth.models import User
import numpy
import random


# Create your views here.
class BoardCreationMixin(object):
    def create_board(self):
        arr = numpy.chararray((15, 15), unicode=True)
        arr[:] = '*'
        b = Board.objects.create(board=arr)
        return b.id


class FindRoomView(View):
    def get(self, request):

        context = {'rooms': Room.objects.all()}
        return render(request, "boards/find.html", context)


class CreateRoomView(BoardCreationMixin, View):
    def post(self, request):
        new_board = self.create_board()
        hand = []
        new_room = Room(board_id=new_board, creator=request.user, creator_hand=hand, turn=request.user.username)

        for i in range(7):
            letter = random.choice(new_room.bag)
            new_room.creator_hand.append(letter)
            new_room.bag.remove(letter)

        new_room.save()

        return redirect('boards:find')


class GameRoomView(View):
    def get(self, request, room_id):

        room_object = Room.objects.get(pk=room_id)
        board = Board.objects.get(room__pk=room_id).board
        own_score, their_score, own_hand = 0, 0, []

        if room_object.creator.id == request.user.id:
            own_score = room_object.creator_score
            their_score = room_object.other_score
            own_hand = room_object.creator_hand
            their_hand = room_object.other_hand

        else:
            if room_object.player_count == 2:
                own_score = room_object.other_score
                their_score = room_object.creator_score
                own_hand = room_object.other_hand
                their_hand = room_object.creator_hand

            else:
                room_object.other = request.user
                room_object.other_score = own_score = 0
                room_object.other_hand = []
                their_score = room_object.creator_score

                for i in range(7):
                    letter = random.choice(room_object.bag)
                    room_object.other_hand.append(letter)
                    room_object.bag.remove(letter)

                room_object.player_count += 1
                room_object.save()

                own_hand = room_object.other_hand
                their_hand = room_object.creator_hand


        context = {'board': board,
                   'creator_id': room_object.creator_id,
                   'own_score': own_score,
                   'their_score': their_score,
                   'own_hand': own_hand,
                   'their_hand': their_hand,
                   'turn': room_object.turn,
                   'room': room_id}
        return render(request, "boards/game.html", context)


class NewBoardView(BoardCreationMixin, View):
    def post(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        Board.objects.get(room__pk=room_id).delete()
        room.board_id = self.create_board()
        new_bag = BAG
        room.creator_score = 0
        room.other_score = 0

        other_hand, creator_hand = [], []
        for i in range(7):
            letter = random.choice(new_bag)
            other_hand.append(letter)
            new_bag.remove(letter)

        for j in range(7):
            letter = random.choice(new_bag)
            creator_hand.append(letter)
            new_bag.remove(letter)

        room.bag = new_bag
        room.creator_hand = creator_hand
        room.other_hand = other_hand
        room.turn = request.user.username
        room.save()

        if request.user.id == room.creator_id:
            own_hand = room.creator_hand
            own_score = room.creator_score
            their_hand = room.other_hand
            their_score = room.other_score
        else:
            own_hand = room.other_hand
            own_score = room.other_score
            their_hand = room.creator_hand
            their_score = room.creator_score

        b = Board.objects.get(room__pk=room_id).board

        context = {'board': b,
                   'own_score': own_score,
                   'their_score': their_score,
                   'own_hand': own_hand,
                   'their_hand': their_hand,
                   'turn': room.turn,
                   'room': room_id}

        return render(request, "boards/game.html", context)
