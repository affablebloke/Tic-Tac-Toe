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
    :return: A Boolean
    """
    state = game.state
    return (state.num_noughts() + state.num_crosses()) == 0


def second_turn(game):
    """
    :param game: The current game.
    :return: A Boolean
    """
    state = game.state
    return (state.num_noughts() + state.num_crosses()) == 1


def bitmask_to_board_position(bitmask):
    """
    |  A |  B |  C |
    ----------------
    |{a1}|{b1}|{c1}|
    |{a2}|{b2}|{c2}|
    |{a2}|{b3}|{c3}|

    :param bitmask: A bitmask converted into a board position. IE 0b000000001 -> 'c3'
    :return: A board position string
    """
    iter_bitmask = 0b000000001
    prefix = 'a'
    for i in range(1, 10):
        if bitmask == iter_bitmask:
            col = ((9 - i) % 3) + 1
            if col == 1:
                prefix = 'a'
            elif col == 2:
                prefix = 'b'
            elif col == 3:
                prefix = 'c'

            return "{0}{1}".format(prefix, str(col))

        iter_bitmask <<= 1

    return None


def first_move(game, team):
    """
    http://en.wikipedia.org/wiki/Tic-tac-toe

    The first player, whom we shall designate "X", has 3 possible positions to mark during the first turn.
    Superficially, it might seem that there are 9 possible positions, corresponding to the 9 squares in the grid.
    However, by rotating the board, we will find that in the first turn, every corner mark is strategically equivalent
    to every other corner mark. The same is true of every edge mark. For strategy purposes, there are therefore only
    three possible first marks: corner, edge, or center. Player X can win or force a draw from any of these starting
    marks; however, playing the corner gives the opponent the smallest choice of squares which must be played to
    avoid losing.

    :param game: The current game.
    :param team: The team to check for 'X' or 'O'.
    :return: void
    """
    other_team = 'X' if team != 'X' else 'O'


def available_corner_moves(game):
    """
    |  A |  B |  C |
    ----------------
    | 1  |    | 2  |
    |    |    |    |
    | 3  |    | 4  |

    :param game: The current game.
    :return: List of available corners
    """
    state = game.state
    corners = [0b100000000, 0b001000000, 0b000000100, 0b000000001]
    return [corner for corner in corners if (corner & state.board_positions_available_bitmask()) > 0]


def available_edge_moves(game):
    """
    |  A |  B |  C |
    ----------------
    |    | 1  |    |
    | 2  |    | 3  |
    |    | 4  |    |

    :param game: The current game.
    :return: List of available edges.
    """
    state = game.state
    edges = [0b010000000, 0b000100000, 0b000001000, 0b000000010]
    return [edge for edge in edges if (edge & state.board_positions_available_bitmask()) > 0]


def center_available(game):
    """
    |  A |  B |  C |
    ----------------
    |    |    |    |
    |    |  X |    |
    |    |    |    |

    :param game: The current game.
    :return: A Boolean.
    """
    state = game.state
    # Why not just use bit masks since they're everywhere, instead of b2 is not None
    return (state.board_positions_available_bitmask() & 0b000010000) > 0


def available_win_moves(game, team):
    """
    |  A |  B |  C |
    ----------------
    |{a1}|{b1}|{c1}|
    |{a2}|{b2}|{c2}|
    |{a2}|{b3}|{c3}|

    MSB -> LSB == a1 -> c3

    :param game: The current game.
    :param team: The team to check for 'X' or 'O'.
    :return: List of bitmasks of available win strategies.
    """
    available_win_list = []
    state = game.state
    team_bitmask = state.crosses_bitmask() if team == 'X' else state.noughts_bitmask()
    available_moves_bitmask = state.board_positions_available_bitmask()
    diagnol_win_bitmask = 0b100010001
    iter_bitmask = 0b000000001
    available_wins_bitmask = 0b000000000

    for i in range(1, 10):
        # Only check for available board positions
        if available_moves_bitmask & iter_bitmask != 0:
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
                col_win_bitmask <<= 1

        iter_bitmask <<= i

    if len(available_win_list) == 0:
        return None
    else:
        return available_win_list
