import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import random
from django.contrib.auth.models import User
from .models import *
from .constants import *


class UpdateBoardConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_id = None
        self.room_group_name = None

    def connect(self):
        print("Connect is called")

        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = "room_%s" % self.room_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        hand = []
        room_object = Room.objects.get(id=self.room_id)
        if room_object.creator.id == self.scope['user'].id:
            own_hand = room_object.creator_hand
            their_hand = room_object.other_hand
        else:
            own_hand = room_object.other_hand
            their_hand = room_object.creator_hand

        # send to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": 'joined',
                                   'data': {'user': self.scope['user'].username,
                                            'own-hand': own_hand, 'their-hand': their_hand}}
        )

        # alper's hand in room 10: ['A', 'V', 'A', 'U', 'L', 'H', 'A']
        self.accept()

    def disconnect(self, close_code):
        print("Disconnect is called")

        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):

        # Access the room and board objects #
        room_id = self.scope['url_route']['kwargs']['room_id']
        board_object = Board.objects.get(room__pk=room_id)
        room_object = Room.objects.get(pk=room_id)

        # Get the message inputs #
        message_inputs = json.loads(text_data)
        word = message_inputs["word"]
        locations = message_inputs["locations"]
        filled_locations = message_inputs["full_locations"]
        existing_letters = message_inputs["existing_letters"]

        # For easier access, create a dictionary with the filled_locations as keys and existing_letters as values #
        location_to_letters = {filled_locations[i]: existing_letters[i] for i in range(len(filled_locations))}

        # Avoid empty words #
        if not word:
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": 'fail', "message": 'Please enter a combination.'}
            )
            return

        # Check if word matches to one in the dictionary #
        # if word.upper() not in DICTIONARY:
        #    self.send(text_data=json.dumps({"type": 'fail',
        #                                   "message": 'Sorry, this word is not valid.'}))
        #    return

        # Initialize variables: #
        # prev_row and prev_column are used to make sure the word is left-to-right or top-to-bottom
        # word_score contains the total score of the word
        # word_multiplier is used to multiply word_score after the letter score calculations are done
        # center flag makes sure the first word is on the center tile (8, 8)
        # is_word_multiplier flag makes sure word_score is multiplied later
        prev_row, prev_column, word_score, word_multiplier = 0, 0, 0, 1
        center, is_word_multiplier = False, False
        check_vertical = check_horizontal = ""
        check_around_score = 0
        new_words = []

        for counter, location in enumerate(locations):
            # Parse locations #
            slice_index = location.find('/')
            curr_row = int(location[:slice_index])
            curr_column = int(location[slice_index + 1:])

            if room_object.turn == self.scope['user'].username:
                creator_get_room = User.objects.get(id=self.scope['user'].id).creator.filter(id=room_id)
                if creator_get_room.exists():
                    room_object.creator_hand.remove(word[counter].upper())
                else:
                    room_object.other_hand.remove(word[counter].upper())
            else:
                msg = self.scope['user'].username + ', please wait for your turn.'
                # Send message to room group
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name, {"type": 'fail', "message": msg}
                )
                return

            # Get the multiplier values from BOARD_SCORES object for each cell #
            if BOARD_SCORES[curr_row - 1][curr_column - 1] == '':
                score_multiplier = 1
                multiplied_obj = 'L'
            else:
                score_multiplier = int(BOARD_SCORES[curr_row - 1][curr_column - 1][0])
                multiplied_obj = BOARD_SCORES[curr_row - 1][curr_column - 1][1]

            # Check if any of the chosen locations is the center #
            if curr_row == 8 and curr_column == 8:
                center = True

            # Conditions for the word placements #
            is_horizontal = (prev_row == curr_row) and (prev_column == curr_column - 1)
            is_vertical = (prev_column == curr_column) and (prev_row == curr_row - 1)
            first_letter = (counter == 0)
            last_letter = (counter == len(word)-1)

            if is_horizontal or is_vertical or first_letter:

                direction = 0

                if is_horizontal:
                    check_vertical = ""

                if is_vertical:
                    check_horizontal = ""

                while direction < 4:
                    check_around_word = ""
                    check_row = check_column = 0

                    if direction == 0 and (is_vertical or first_letter or (is_vertical and last_letter)):
                        check_row = curr_row
                        check_column = curr_column - 1
                        print("go left")

                    elif direction == 1 and (is_horizontal or first_letter or (is_horizontal and last_letter)):
                        check_row = curr_row - 1
                        check_column = curr_column
                        print("go above")


                    elif direction == 2 and (is_vertical or first_letter or last_letter):
                        check_row = curr_row
                        check_column = curr_column + 1
                        print("go right")


                    elif direction == 3 and (is_horizontal or first_letter or last_letter):
                        check_row = curr_row + 1
                        check_column = curr_column
                        print("go below")

                    print("row: %d | col: %d" % (check_row, check_column))

                    while (1 <= check_column <= 15) and (1 <= check_row <= 15):
                        letter = board_object.board[check_row-1][check_column-1]

                        if direction == 0:
                            if letter != '*':
                                check_around_word = letter + check_around_word
                                check_around_score += Letter.objects.get(pk=letter).score
                            else:
                                break
                            check_column -= 1
                            print("checking cells on left")

                        elif direction == 1:
                            if letter != '*':
                                check_around_word = letter + check_around_word
                                check_around_score += Letter.objects.get(pk=letter).score
                            else:
                                break
                            check_row -= 1
                            print("checking cells above")

                        elif direction == 2:
                            if letter != '*':
                                check_around_word = check_around_word + letter
                                check_around_score += Letter.objects.get(pk=letter).score
                            else:
                                break
                            check_column += 1
                            print("checking cells on right")

                        elif direction == 3:
                            if letter != '*':
                                check_around_word = check_around_word + letter
                                check_around_score += Letter.objects.get(pk=letter).score
                            else:
                                break
                            check_row += 1
                            print("checking cells below")


                    print("the word %s" % check_around_word)

                    if direction == 0:
                        if is_horizontal or last_letter:
                            check_horizontal += word[counter].upper()
                        else:
                            check_horizontal = check_around_word + word[counter].upper() + check_horizontal

                    elif direction == 1:
                        if is_vertical or last_letter:
                            check_vertical += word[counter].upper()
                        else:
                            check_vertical = check_around_word + word[counter].upper() + check_vertical

                    elif direction == 2:
                        if check_horizontal == "":
                            check_horizontal = word[counter].upper() + check_around_word
                        else:
                            check_horizontal = check_horizontal + check_around_word

                    elif direction == 3:
                        if check_vertical == "":
                            check_vertical = word[counter].upper() + check_around_word
                        else:
                            check_vertical = check_vertical + check_around_word

                    direction += 1

                if first_letter:
                    if check_vertical:
                        print("Vertical word w/ letter %d: %s" % (counter, check_vertical))
                        if len(check_vertical) > 1:
                            new_words.append(check_vertical)
                    if check_horizontal:
                        print("Vertical word w/ letter %d: %s" % (counter, check_horizontal))
                        if len(check_horizontal) > 1:
                            new_words.append(check_horizontal)

                if is_horizontal:
                    print("Vertical word w/ letter %d: %s" % (counter, check_vertical))
                    # Check if word matches to one in the dictionary #
                    # if check_vertical not in DICTIONARY:
                    #    msg = 'Sorry, %s is not a legal word.' % check_vertical
                    #    self.send(text_data=json.dumps({"type": 'fail', "message": msg}))
                    #    return
                    if len(check_vertical) > 1:
                        new_words.append(check_vertical)

                    if last_letter:
                        print("Full horizontal word: " + check_horizontal)
                        # Check if word matches to one in the dictionary #
                        # if check_horizontal not in DICTIONARY:
                        #    msg = 'Sorry, %s is not a legal word.' % check_horizontal
                        #    self.send(text_data=json.dumps({"type": 'fail', "message": msg}))
                        #    return
                        if len(check_horizontal) > 1:
                            new_words.append(check_horizontal)

                if is_vertical:
                    print("Horizontal word w/ letter %d: %s" % (counter, check_horizontal))
                    # Check if word matches to one in the dictionary #
                    # if check_horizontal not in DICTIONARY:
                    #    msg = 'Sorry, %s is not a legal word.' % check_horizontal
                    #    self.send(text_data=json.dumps({"type": 'fail', "message": msg}))
                    #    return
                    if len(check_horizontal) > 1:
                        new_words.append(check_horizontal)

                    if last_letter:
                        print("Full vertical word: " + check_vertical)
                        # Check if word matches to one in the dictionary #
                        # if check_vertical not in DICTIONARY:
                        #    msg = 'Sorry, %s is not a legal word.' % check_vertical
                        #    self.send(text_data=json.dumps({"type": 'fail', "message": msg}))
                        #    return
                        if len(check_vertical) > 1:
                            new_words.append(check_vertical)

                if location not in filled_locations:
                    board_object.board[curr_row - 1][curr_column - 1] = word[counter].upper()
                else:
                    # If the letter already exists on the board, only add its letter value
                    # to word_score regardless of the board scores
                    # word_score += Letter.objects.get(pk=location_to_letters[location]).score
                    prev_row, prev_column = curr_row, curr_column
                    continue

                if multiplied_obj == 'L':
                    word_score += Letter.objects.get(pk=word[counter].upper()).score * score_multiplier

                elif multiplied_obj == 'W':
                    is_word_multiplier = True
                    word_multiplier *= score_multiplier
                    word_score += Letter.objects.get(pk=word[counter].upper()).score

                prev_row, prev_column = curr_row, curr_column

            else:
                msg = 'Cells should be chosen in the same row left-to-right, or in the same column top-to-down.'
                # Send message to room group
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name, {"type": 'fail', "message": msg}
                )
                return


        if board_object.is_empty and not center:
            msg = 'Please start the game using the center tile.'
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": 'fail', "message": msg}
            )
            return

        if board_object.is_empty:
            board_object.is_empty = False

        if is_word_multiplier:
            word_score *= word_multiplier

        if self.scope['user'].id == room_object.creator_id:
            room_object.creator_score += word_score + check_around_score
            for i in range(len(word)):
                letter = random.choice(room_object.bag)
                room_object.creator_hand.append(letter)
                room_object.bag.remove(letter)

            new_tiles = room_object.creator_hand
            score = room_object.creator_score
            room_object.turn = room_object.other.username

        else:
            room_object.other_score += word_score + check_around_score
            for i in range(len(word)):
                letter = random.choice(room_object.bag)
                room_object.other_hand.append(letter)
                room_object.bag.remove(letter)

            new_tiles = room_object.other_hand
            score = room_object.other_score
            room_object.turn = room_object.creator.username



        board_object.save()
        room_object.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": 'success',
                                   'data': {'user': User.objects.get(username=self.scope['user']).id,
                                            'score': score, 'turn': room_object.turn,
                                            'word': word, 'locations': locations,
                                            'new_tiles': new_tiles, 'new_words': new_words}}
        )

    # Receive message from room group
    def fail(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"type": event["type"], "message": message}))

    def success(self, event):
        data = event["data"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"type": event["type"], "data": data}))

    def joined(self, event):
        data = event["data"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"type": event["type"], "data": data}))

