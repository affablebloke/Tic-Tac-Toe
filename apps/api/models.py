import random
from django.db import models
from utils import base58
from datetime import datetime


class GameState(models.Model):
    """
    By keeping game state on the server, this makes it easier to build other dummy clients (iOS/Android) and helps
    resolve game game state issues if you want to build multi-player functionality. Also, using easy to read columns
    and rows makes it easier to read than using bitmasks.

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

    last_move_x = models.CharField(max_length=1, null=True)
    last_move_o = models.CharField(max_length=1, null=True)

    def cells(self):
        """
        |  A |  B |  C |
        ---------------
        |{a1}|{b1}|{c1}|
        |{a2}|{b2}|{c2}|
        |{a2}|{b3}|{c3}|
        :return: A list in Matrix like order.
        """
        return [self.a1, self.b1, self.c1, self.a2, self.b2, self.c2, self.a3, self.b3, self.c3]

    def num_crosses(self):
        return len([cross for cross in self.crosses() if cross == 1])

    def crosses(self):
        """
        A utility function to check crosses.
        :return: A list of crosses a1->c3 with values 1, meaning cross, or 0
        """
        return [self.isCross(v) for v in self.cells()]

    def crosses_bitmask(self):
        """
        A utility function to convert crosses to a bitmask.
        :return: A 9 bit bitmask. a1->c3
        """
        return int("".join(str(x) for x in self.crosses()), 2)

    def num_noughts(self):
        return len([nought for nought in self.noughts() if nought == 1])

    def noughts(self):
        """
        A utility function to check noughts.
        :return: A list of noughts a1->c3 with values 1, meaning nought, or 0
        """
        return [self.isNought(v) for v in self.cells()]

    def noughts_bitmask(self):
        """
        A utility function to convert noughts to a bitmask.
        :return: A 9 bit bitmask. a1->c3
        """
        return int("".join(str(x) for x in self.noughts()), 2)

    def isNought(self, value):
        if value is None:
            return 0
        else:
            return 1 if value.lower() == "o" else 0

    def isCross(self, value):
        if value is None:
            return 0
        else:
            return 1 if value.lower() == "x" else 0

    def board_positions_available_bitmask(self):
        """
        A utility function to check for available slots.
        :return: A 9 bit bitmask. a1->c3
        """
        return ~(self.crosses_bitmask() | self.noughts_bitmask()) & 0b111111111

    def reset(self):
        """
        Resets the game board state.
        :return: void
        """
        self.a1 = self.a2 = self.a3 = None
        self.b1 = self.b2 = self.b3 = None
        self.c1 = self.c2 = self.c3 = None
        self.last_move_x = self.last_move_o = None

    def __str__(self):
        return """
            |A|B|C|
            -------
            |{a1}|{b1}|{c1}|
            |{a2}|{b2}|{c2}|
            |{a2}|{b3}|{c3}|
        """.format(**self.__dict__)


class PlayerType(models.Model):
    """
    Keeps track of Player information.
    """
    # NOUGHT or CROSS
    team = models.CharField(max_length=1)
    is_human = models.BooleanField(default=False)


class TicTacToeGame(models.Model):
    """
    By keeping game state on the server, this makes it easier to build other dummy clients (iOS/Android) and helps resolve
    game game state issues if you want to build multi-player functionality.
    """
    token = models.CharField(max_length=60)
    game_state = models.OneToOneField(GameState, related_name='game_state')
    # For now player_1 is always human
    player_1 = models.OneToOneField(PlayerType, related_name='player_1')
    player_2 = models.OneToOneField(PlayerType, related_name='player_2')
    created = models.DateTimeField(default=datetime.utcnow())

    @classmethod
    def create(cls, **kwargs):
        game = cls(**kwargs)
        player_1 = PlayerType(team='X', is_human=True)
        player_2 = PlayerType(team='O', is_human=False)
        player_1.save()
        player_2.save()
        game.player_1 = player_1
        game.player_2 = player_2
        game_state = GameState()
        game_state.save()
        game.game_state = game_state
        game.token = base58.b58encode(str(random.randrange(999, 9999999, 2)))
        return game
