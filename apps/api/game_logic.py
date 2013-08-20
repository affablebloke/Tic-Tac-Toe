from apps.api.models import GameState
import owyl
import random

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


class AI(object):
    """
    The brains behind this Tic-Tac-Toe implementation. I know behavior trees is overkill for this Tic-Tac-Toe,
    but they're fun to work with.
    """

    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.tree = self.buildTree()

    def buildTree(self):
        """
        Build the behavior tree.
        """
        owyl.selector
        tree = owyl.selector(owyl.sequence(self.is_first_move(),
                                           self.calculate_first_move()),
                             owyl.sequence(self.is_win_move_available(),
                                           self.calculate_win_move()))

        return owyl.visit(tree)

    def run(self):
        for value in self.tree:
            pass

    @owyl.taskmethod
    def is_first_move(self, **kwargs):
        """
        Determines if its the first move.
        """
        is_first_move = False
        if self.player.team == 'X':
            is_first_move = self.game.state.last_move_x is None
        else:
            is_first_move = self.game.state.last_move_o is None

        yield is_first_move

    @owyl.taskmethod
    def calculate_first_move(self, **kwargs):
        """
        Finds the best first move.
        """
        other_player_last_move = self.game.state.last_move_x if self.player.team == 'O' else self.game.state.last_move_o
        if other_player_last_move is None:
            # Choose a random corner
            moves = self.available_corner_moves()
            position_bitmask = moves[random.randrange(0, len(moves))]
            position = self.bitmask_to_board_position(position_bitmask)
            self.mark_position(position)
        else:
            # AI should take the center
            if self.center_available():
                self.mark_position('b2')
            else:
                # AI should take a corner
                moves = self.available_corner_moves(game)
                position_bitmask = moves[random.randrange(0, len(moves))]
                position = self.bitmask_to_board_position(position_bitmask)
                self.mark_position(position)

        yield True

    @owyl.taskmethod
    def is_win_move_available(self, **kwargs):
        """
        Simply finds if there is a win move available.
        """
        yield self.available_win_moves() is not None

    @owyl.taskmethod
    def calculate_win_move(self, **kwargs):
        """
        Choose a win move.
        """
        # AI should take a corner
        moves = self.available_win_moves()
        position_bitmask = moves[random.randrange(0, len(moves))]
        position = self.bitmask_to_board_position(position_bitmask)
        self.mark_position(position)
        yield True

    def first_turn(self):
        """
        :return: A Boolean
        """
        return (self.game.state.num_noughts() + self.game.state.num_crosses()) == 0

    def second_turn(self):
        """
        :return: A Boolean
        """
        return (self.game.state.num_noughts() + self.game.state.num_crosses()) == 1

    def bitmask_to_board_position(self, bitmask):
        """
        |  A |  B |  C |
        ----------------
        |{a1}|{b1}|{c1}|
        |{a2}|{b2}|{c2}|
        |{a3}|{b3}|{c3}|

        :param bitmask: A bitmask converted into a board position. IE 0b000000001 -> 'c3'
        :return: A board position string
        """
        iter_bitmask = 0b000000001
        prefix = 'a'
        for i in range(1, 10):
            if bitmask == iter_bitmask:
                col = i % 3
                if col == 0:
                    prefix = 'a'
                elif col == 1:
                    prefix = 'c'
                elif col == 2:
                    prefix = 'b'

                row = 3
                if bitmask > 0b000100000:
                    row = 1
                elif bitmask > 0b000000100:
                    row = 2

                return "{0}{1}".format(prefix, row)

            iter_bitmask <<= 1

        return None

    def first_move(self):
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
        :param player: The player to check for 'X' or 'O'.
        """
        other_player = 'X' if player != 'X' else 'O'

    def available_corner_moves(self):
        """
        |  A |  B |  C |
        ----------------
        | 1  |    | 2  |
        |    |    |    |
        | 3  |    | 4  |

        :return: List of available corners
        """
        corners = [0b100000000, 0b001000000, 0b000000100, 0b000000001]
        return [corner for corner in corners if (corner & self.game.state.board_positions_available_bitmask()) > 0]

    def available_edge_moves(self):
        """
        |  A |  B |  C |
        ----------------
        |    | 1  |    |
        | 2  |    | 3  |
        |    | 4  |    |

        :return: List of available edges.
        """
        edges = [0b010000000, 0b000100000, 0b000001000, 0b000000010]
        return [edge for edge in edges if (edge & self.game.state.board_positions_available_bitmask()) > 0]

    def center_available(self):
        """
        |  A |  B |  C |
        ----------------
        |    |    |    |
        |    |  X |    |
        |    |    |    |

        :return: A Boolean.
        """
        # Why not just use bit masks since they're everywhere, instead of b2 is not None
        return (self.game.state.board_positions_available_bitmask() & 0b000010000) > 0

    def mark_position(self, position, player=None):
        """
        |  A |  B |  C |
        ----------------
        |{a1}|{b1}|{c1}|
        |{a2}|{b2}|{c2}|
        |{a3}|{b3}|{c3}|

        :param position: A property string
        """
        if player is None:
            player = self.player

        if player.team == 'X':
            self.game.state.last_move_x = position
        else:
            self.game.state.last_move_o = position

        self.game.state.__setattr__(position, player.team)

    def available_win_moves(self):
        """
        |  A |  B |  C |
        ----------------
        |{a1}|{b1}|{c1}|
        |{a2}|{b2}|{c2}|
        |{a3}|{b3}|{c3}|

        MSB -> LSB == a1 -> c3

        :return: List of bitmasks of available win strategies.
        """
        available_win_list = []
        player_bitmask = self.game.state.crosses_bitmask() if self.player.team == 'X' else self.game.state.noughts_bitmask()
        available_moves_bitmask = self.game.state.board_positions_available_bitmask()
        diagnol_win_bitmask = 0b100010001
        iter_bitmask = 0b000000001
        available_wins_bitmask = 0b000000000

        for i in range(1, 10):
            # Only check for available board positions
            if available_moves_bitmask & iter_bitmask != 0:
                test = iter_bitmask | player_bitmask

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