from apps.api.models import GameState

"""
http://en.wikipedia.org/wiki/Tic-tac-toe

A player can play perfect Tic-tac-toe (win or draw) given they choose the first possible move from the following list.

Win: If the player has two in a row, they can place a third to get three in a row.
Block: If the [opponent] has two in a row, the player must play the third themself to block the opponent.
Fork: Create an opportunity where the player has two threats to win (two non-blocked lines of 2).
Blocking an opponent's fork:
    Option 1: The player should create two in a row to force the opponent into defending, as long as it doesn't result in
                them creating a fork. For example, if "X" has a corner, "O" has the center, and "X" has the opposite
                corner as well, "O" must not play a corner in order to win.
                 (Playing a corner in this scenario creates a fork for "X" to win.)

    Option 2: If there is a configuration where the opponent can fork, the player should block that fork.

Center: A player marks the center. (If it is the first move of the game, playing on a corner gives "O" more
 opportunities to make a mistake and may therefore be the better choice; however, it makes no difference between
  perfect players.)
Opposite corner: If the opponent is in the corner, the player plays the opposite corner.
Empty corner: The player plays in a corner square.
Empty side: The player plays in a middle square on any of the 4 sides.


"""


def get_props(game):
     # TODO(daniel): This will introduce a bug with any other property names starting with a, b, or c
    props = dict((k, v) for k, v in game.state.__dict__.iteritems() if (k.startswith('a') or k.startswith('b')
                                                                        or k.startswith('c')))
    return props


def first_turn(game):
    """
    :param game: The current game.
    :return: A Boolean representing if its the first move.
    """
    props = get_props(game)
    values = [x for x in props.values() if x is not None]
    return len(values) == 0


def second_turn(game):
    """
    :param game: The current game.
    :return: A Boolean representing if its the second move.
    """
    props = get_props(game)
    values = [x for x in props.values() if x is not None]
    return len(values) == 1
