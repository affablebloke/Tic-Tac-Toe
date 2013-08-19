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


def first_turn(game):
    """
    :param game: The current game.
    :return: A Boolean representing if its the first move.
    """
    state = game.state
    return (state.num_noughts() + state.num_crosses()) == 0


def second_turn(game):
    """
    :param game: The current game.
    :return: A Boolean representing if its the second move.
    """
    state = game.state
    return (state.num_noughts() + state.num_crosses()) == 1


def bitmask_to_slot(bitmask):
    """
    |  A |  B |  C |
    ---------------
    |{a1}|{b1}|{c1}|
    |{a2}|{b2}|{c2}|
    |{a2}|{b3}|{c3}|

    :param bitmask: A bitmask converted into a board slot. IE 0b000000001 -> 'c3'
    :return: A slot string
    """
    pass

def available_win_slot(game, team):
    """
    |  A |  B |  C |
    ---------------
    |{a1}|{b1}|{c1}|
    |{a2}|{b2}|{c2}|
    |{a2}|{b3}|{c3}|

    MSB -> LSB == a1 -> c3

    :param game: The current game.
    :param team: The team to check for 'X' or 'O'.
    :return: List of masks of available win strategies.
    """
    available_win_list = []
    state = game.state
    team_bitmask = state.crosses_bitmask() if team == 'X' else state.noughts_bitmask()
    available_slots_bitmask = state.slots_available_bitmask()
    diagnol_win_bitmask = 0b100010001
    iter_bitmask = 0b000000001
    available_wins_bitmask = 0b000000000

    for i in range(1, 10):
        # Only check for available slots
        if available_slots_bitmask & iter_bitmask != 0:
            test = iter_bitmask | team_bitmask

            #check for diagnol win
            if test & diagnol_win_bitmask == diagnol_win_bitmask:
                available_win_list.append(iter_bitmask)
                available_wins_bitmask |= iter_bitmask

            col_win_bitmask = 0b001001001
            row_win_bitmask = 0b000000111
            for j in range(1, 4):
                #check for col win
                if test & col_win_bitmask == col_win_bitmask:
                    available_win_list.append(iter_bitmask)
                    available_wins_bitmask |= iter_bitmask

                #check for row win
                if test & row_win_bitmask == row_win_bitmask:
                    available_win_list.append(iter_bitmask)
                    available_wins_bitmask |= iter_bitmask

                row_win_bitmask <<= 3
                col_win_bitmask <<= j

        iter_bitmask <<= i

    if len(available_win_list) == 0:
        return None
    else:
        return available_win_list
