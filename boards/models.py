from django.db import models
from picklefield.fields import PickledObjectField
from django.conf import settings
from .constants import BAG


# Create your models here.
class Letter(models.Model):
    letter = models.CharField(max_length=3, primary_key=True)
    score = models.IntegerField()

    def __str__(self):
        return self.letter


class Board(models.Model):
    board = PickledObjectField()
    is_empty = models.BooleanField(default=True)


class Room(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    bag = PickledObjectField(default=BAG)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="creator", on_delete=models.PROTECT)
    creator_hand = PickledObjectField()
    creator_score = models.IntegerField(default=0)
    other = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="other", on_delete=models.PROTECT, null=True)
    other_hand = PickledObjectField(null=True)
    other_score = models.IntegerField(null=True)
    player_count = models.IntegerField(default=1)
    turn = models.CharField(null=True)


class Leaderboard(models.Model):
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    overall_score = models.IntegerField(default=0)

