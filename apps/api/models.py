from django.db import models
from utils import base58
from datetime import datetime


class GameState(models.Model):
    """
    By keeping game state on the server, this makes it easier to build other dummy clients (iOS/Android) and helps resolve
    game game state issues if you want to build multi-player functionality.

    |A|B|C|
    -------
    |O|X|X|
    |X|O|O|
    |X|O|X|

    """
    a1 = models.CharField(max_length=1, null=True)
    a2 = models.CharField(max_length=1, null=True)
    a3 = models.CharField(max_length=1, null=True)
    b1 = models.CharField(max_length=1, null=True)
    b2 = models.CharField(max_length=1, null=True)
    b3 = models.CharField(max_length=1, null=True)
    c1 = models.CharField(max_length=1, null=True)
    c2 = models.CharField(max_length=1, null=True)
    c3 = models.CharField(max_length=1, null=True)


class PayerType(models.Model):
    """
    Keeps track of Player information.
    """
    TEAM_CHOICES = ["NOUGHT", "CROSS"]
    # NOUGHT or CROSS
    team = models.CharField(max_length=6)
    is_human = models.BooleanField(default=False)


class TicTacToeGame(models.Model):
    """
    By keeping game state on the server, this makes it easier to build other dummy clients (iOS/Android) and helps resolve
    game game state issues if you want to build multi-player functionality.
    """
    state = models.OneToOneField(GameState, related_name='state')
    # For now player_1 is always human
    player_1 = models.OneToOneField(PayerType, related_name='p1')
    player_2 = models.OneToOneField(PayerType, related_name='p2')
    token = models.CharField(max_length=60)
    created = models.DateTimeField(default=datetime.utcnow())