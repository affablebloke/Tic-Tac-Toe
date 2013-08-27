from apps.api.models import GameState
import owyl
import random

"""
http://en.wikipedia.org/wiki/Tic-tac-toe

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
        tree = owyl.selector(
                             owyl.sequence(self.is_win_move_available(),
                                           self.play_win_move()),
                             owyl.sequence(self.is_block_move_available(),
                                           self.play_block_move()),
                             owyl.sequence(self.is_fork_available(),
                                           self.play_fork_move()),
                             owyl.sequence(self.is_block_fork_available(),
                                           self.play_block_fork_move()),
                             owyl.sequence(self.is_center_available(),
                                           self.play_center()),
                             owyl.sequence(self.is_opposite_corner_available(),
                                           self.play_opposite_corner_move()),
                             owyl.sequence(self.is_corner_available(),
                                           self.play_corner_move()),
                             owyl.sequence(self.is_edge_available(),
                                           self.play_edge_move())
        )

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
            is_first_move = self.game.game_state.last_move_x is None
        else:
            is_first_move = self.game.game_state.last_move_o is None

        yield is_first_move

    @owyl.taskmethod
    def play_first_move(self, **kwargs):
        """
        Finds the best first move.
        """
        other_player_last_move = self.game.game_state.last_move_x if self.player.team == 'O' else self.game.game_state.last_move_o
        if other_player_last_move is None:
            # Choose a random corner
            moves = self.available_corner_moves()
            position_bitmask = moves[random.randrange(0, len(moves))]
            position = self.bitmask_to_board_position(position_bitmask)
            self.mark_position(position)
        else:

            if self.is_corner_position(other_player_last_move):
                position = self.available_opposite_corner()
                self.mark_position(position)
            else:
                # AI should take a corner
                moves = self.available_corner_moves()
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
    def play_win_move(self, **kwargs):
        """
        Play a win move.
        """
        # AI should take a corner
        moves = self.available_win_moves()
        position_bitmask = moves[random.randrange(0, len(moves))]
        position = self.bitmask_to_board_position(position_bitmask)
        self.mark_position(position)
        yield True

    @owyl.taskmethod
    def is_block_move_available(self, **kwargs):
        """
        Determines if the AI should block
        """
        yield self.available_win_moves(player=self.other_team()) is not None

    @owyl.taskmethod
    def play_block_move(self, **kwargs):
        """
        Play a block move.
        """
        moves = self.available_win_moves(player=self.other_team())
        position_bitmask = moves[random.randrange(0, len(moves))]
        position = self.bitmask_to_board_position(position_bitmask)
        self.mark_position(position)
        yield True

    @owyl.taskmethod
    def is_corner_available(self, **kwargs):
        """
        Simply finds if there is a corner available.
        """
        yield len(self.available_corner_moves()) > 0

    @owyl.taskmethod
    def play_corner_move(self, **kwargs):
        """
        Play a corner move.
        """
        moves = self.available_corner_moves()
        position_bitmask = moves[random.randrange(0, len(moves))]
        position = self.bitmask_to_board_position(position_bitmask)
        self.mark_position(position)
        yield True

    @owyl.taskmethod
    def is_center_available(self, **kwargs):
        """
        Simply finds if the center is available
        """
        yield self.game.game_state.b2 is None

    @owyl.taskmethod
    def play_center(self, **kwargs):
        """
        Play a center move.
        """
        self.mark_position('b2')
        yield True

    @owyl.taskmethod
    def is_edge_available(self, **kwargs):
        """
        Simply finds if there is a edge available.
        """
        yield len(self.available_edge_moves()) > 0

    @owyl.taskmethod
    def play_edge_move(self, **kwargs):
        """
        Play an edge move.
        """
        moves = self.available_edge_moves()
        position_bitmask = moves[random.randrange(0, len(moves))]
        position = self.bitmask_to_board_position(position_bitmask)
        self.mark_position(position)
        yield True

    @owyl.taskmethod
    def is_opposite_corner_available(self, **kwargs):
        """
        Simply finds if there is a opposite corner available.
        """
        yield self.available_opposite_corner() is not None

    @owyl.taskmethod
    def play_opposite_corner_move(self, **kwargs):
        """
        Play an opposite corner move.
        """
        position = self.available_opposite_corner()
        self.mark_position(position)

        yield True

    @owyl.taskmethod
    def is_fork_available(self, **kwargs):
        """
        Simply finds if there is a fork move available.
        """
        yield self.available_fork() is not None

    @owyl.taskmethod
    def play_fork_move(self, **kwargs):
        """
        Play a fork move.
        """
        self.mark_position(self.available_fork())
        yield True

    @owyl.taskmethod
    def is_block_fork_available(self, **kwargs):
        """
        Simply finds if there is a block fork move available.
        """
        yield self.available_fork(self.other_team()) is not None

    @owyl.taskmethod
    def play_block_fork_move(self, **kwargs):
        """
        Play a block fork move.
        """
        center = self.game.game_state.b2
        # check to see if you should play a middle position
        if center and center.upper() == self.player.team.upper():
            moves = self.available_edge_moves()
            position_bitmask = moves[random.randrange(0, len(moves))]
            position = self.bitmask_to_board_position(position_bitmask)
            self.mark_position(position)
        else:
            moves = self.available_corner_moves()
            position_bitmask = moves[random.randrange(0, len(moves))]
            position = self.bitmask_to_board_position(position_bitmask)
            self.mark_position(position)

        yield True

    def first_turn(self):
        """
        :return: A Boolean
        """
        return (self.game.game_state.num_noughts() + self.game.game_state.num_crosses()) == 0

    def second_turn(self):
        """
        :return: A Boolean
        """
        return (self.game.game_state.num_noughts() + self.game.game_state.num_crosses()) == 1

    def other_team(self):
        team = self.player.team
        other_team = self.game.player_1
        if other_team.team == team:
            other_team = self.game.player_2

        return other_team

    def is_corner_position(self, position):
        """
        :param position: The position to test
        :return: A Boolean
        """
        corners = ["a1", "c1", "a3", "c3"]
        return position.lower() in corners

    def available_opposite_corner(self):
        """
        Finds an available opposite corner.
        :return: A board position string
        """
        team = self.player.team
        opposite_corner_map = {"a1": "c3", "c3": "a1", "c1": "a3", "a3": "c1"}
        for k in opposite_corner_map.keys():
            if not self.available_position(k) and getattr(self.game.game_state, k) != team and self.available_position(
                    opposite_corner_map[k]):
                return opposite_corner_map[k]

        return None

    def available_fork(self, player=None):
        """
        Finds an available fork.
        :return: A board position string
        """
        if player is None:
            player = self.player

        team = player.team
        opposite_corner_map = {"a1": "c3", "c3": "a1", "c1": "a3", "a3": "c1"}
        for k in opposite_corner_map.keys():
            if getattr(self.game.game_state, opposite_corner_map[k]) == team and\
                            getattr(self.game.game_state, k) == team and len(self.available_corner_moves()) > 0:
                    moves = self.available_corner_moves()
                    return moves[random.randrange(0, len(moves))]

        return None

    def potential_fork(self, player=None):
        """
        Finds an potential fork.
        :return: A board position string
        """
        if player is None:
            player = self.player

        team = player.team
        opposite_corner_map = {"a1": "c3", "c3": "a1", "c1": "a3", "a3": "c1"}
        for k in opposite_corner_map.keys():
            if getattr(self.game.game_state, opposite_corner_map[k]) == team and\
                            getattr(self.game.game_state, k) is None:
                    return k.upper()

        return None

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
        return [corner for corner in corners if (corner & self.game.game_state.board_positions_available_bitmask()) > 0]

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
        return [edge for edge in edges if (edge & self.game.game_state.board_positions_available_bitmask()) > 0]

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
        return (self.game.game_state.board_positions_available_bitmask() & 0b000010000) > 0

    def available_position(self, position):
        """
        Is this position available.

        :param position: The position.
        :return: A Boolean.
        """
        return getattr(self.game.game_state, position) is None

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
            self.game.game_state.last_move_x = position.upper()
        else:
            self.game.game_state.last_move_o = position.upper()

        self.game.game_state.__setattr__(position.lower(), player.team.upper())

    def check_wins(self, player_bitmask, availability_bitmask=None):

        available_win_list = []
        iter_bitmask = 0b000000001
        diagnol_bitmask = 0b100010001
        diagnol_bitmask2 = 0b001010100

        if availability_bitmask is None:
            availability_bitmask = player_bitmask

        for i in range(1, 10):
            # Only check for available board positions
            if availability_bitmask & iter_bitmask != 0:
                test = iter_bitmask | player_bitmask

                #check for diagnols
                if (test & diagnol_bitmask) == diagnol_bitmask or (test & diagnol_bitmask2) == diagnol_bitmask2:
                    available_win_list.append(iter_bitmask)

                col_win_bitmask = 0b001001001
                row_win_bitmask = 0b000000111
                for j in range(1, 4):
                    #check for col win
                    if test & col_win_bitmask == col_win_bitmask:
                        available_win_list.append(iter_bitmask)

                    #check for row win
                    if test & row_win_bitmask == row_win_bitmask:
                        available_win_list.append(iter_bitmask)

                    row_win_bitmask <<= 3
                    col_win_bitmask <<= 1

            iter_bitmask <<= 1

        return available_win_list

    def available_win_moves(self, player=None):
        """
        |  A |  B |  C |
        ----------------
        |{a1}|{b1}|{c1}|
        |{a2}|{b2}|{c2}|
        |{a3}|{b3}|{c3}|

        MSB -> LSB == a1 -> c3

        :return: List of bitmasks of available win strategies.
        """
        if player is None:
            player = self.player

        player_bitmask = self.game.game_state.crosses_bitmask()
        if player.team == 'O':
            player_bitmask = self.game.game_state.noughts_bitmask()

        available_bitmask = self.game.game_state.board_positions_available_bitmask()

        available_win_list = self.check_wins(player_bitmask, availability_bitmask=available_bitmask)

        if len(available_win_list) == 0:
            return None
        else:
            return available_win_list