from django.test.client import Client
from django.test import TestCase
from apps.api.models import TicTacToeGame, PlayerType
import game_logic


class APITest(TestCase):

    def setUp(self):
        self.client = Client()
        self.game = TicTacToeGame.create(player_1=PlayerType(team='X', is_human=True),
                                         player_2=PlayerType(team='O', is_human=False))

    def test_new_game(self):
        """
        Tests new game.
        """
        self.assertIsNotNone(self.game)
        self.assertIsNotNone(self.game.state)
        self.assertIsNotNone(self.game.token)

        self.assertIsNotNone(self.game.player_1)
        self.assertIsNotNone(self.game.player_2)

        self.assertIs(self.game.player_1.is_human, True)
        self.assertIs(self.game.player_2.is_human, False)

        self.assertEqual(self.game.player_1.team, 'X')
        self.assertEqual(self.game.player_2.team, 'O')

    def test_game_state(self):
        """
        Tests game state.
        """
        self.game.state.a1 = 'X'
        self.game.state.a2 = 'X'
        self.game.state.a3 = 'X'

        crosses = self.game.state.crosses()
        self.assertEqual(crosses[0], 1)
        self.assertEqual(crosses[3], 1)
        self.assertEqual(crosses[6], 1)

        self.game.state.reset()
        crosses = self.game.state.crosses()
        self.assertEqual(crosses[0], 0)

    def test_first_turn_logic(self):
        """
        Tests first turn logic.
        """
        self.game.state.reset()

        self.assertIs(game_logic.first_turn(self.game), True)
        self.game.state.a1 = 'X'

        self.assertIs(game_logic.first_turn(self.game), False)

    def test_available_positions_logic(self):

        self.game.state.reset()

        """
        Create board state.
        |A|B|C|
        -------
        |X| | |
        |O| | |
        | | | |
        """
        self.game.state.a1 = 'X'
        self.game.state.a2 = 'O'

        self.assertEqual(self.game.state.crosses_bitmask(), 0b100000000)
        self.assertEqual(self.game.state.noughts_bitmask(), 0b000100000)

        available_positions = ~(0b100000000 | 0b000100000) & 0b111111111
        self.assertEqual(available_positions, self.game.state.board_positions_available_bitmask())

    def test_available_win_moves_logic(self):

        self.game.state.reset()
        print(self.game.state)

        """
        Create board state.
        |A|B|C|
        -------
        |X|X| |
        |O|X| |
        |O| | |
        """
        self.game.state.a1 = 'X'
        self.game.state.a2 = 'O'
        self.game.state.a3 = 'O'
        self.game.state.b1 = 'X'
        self.game.state.b2 = 'X'

        available_wins = game_logic.available_win_moves(self.game, 'X')
        diagnol_win = 0b000000001
        row_win = 0b000000100
        col_win = 0b010000000

        self.assertIsNotNone(diagnol_win in available_wins)
        self.assertIsNotNone(row_win in available_wins)
        self.assertIsNotNone(col_win in available_wins)

    def test_board_bitmask_position_logic(self):

        self.game.state.reset()

        """
        Create board state.
        |A|B|C|
        -------
        |X|X| |
        |O|X| |
        |O| | |
        """
        self.game.state.a1 = 'X'
        self.game.state.a2 = 'O'
        self.game.state.a3 = 'O'
        self.game.state.b1 = 'X'
        self.game.state.b2 = 'X'

        self.assertEqual('c3', game_logic.bitmask_to_board_position(0b000000001))
        self.assertEqual('a1', game_logic.bitmask_to_board_position(0b100000000))

    def test_corners_edges_logic(self):

        self.game.state.reset()

        """
        Create board state.
        |A|B|C|
        -------
        | |X| |
        |O|X| |
        |O| | |
        """
        self.game.state.a2 = 'O'
        self.game.state.a3 = 'O'
        self.game.state.b1 = 'X'
        self.game.state.b2 = 'X'

        available_edges = game_logic.available_edge_moves(self.game)
        self.assertIsNotNone(available_edges[0] in [0b000000010, 0b000001000])
        self.assertIsNotNone(available_edges[1] in [0b000000010, 0b000001000])

        available_corners = game_logic.available_corner_moves(self.game)
        self.assertIsNotNone(available_corners[0] in [0b100000000, 0b001000000, 0b000000001])
        self.assertIsNotNone(available_corners[1] in [0b100000000, 0b001000000, 0b000000001])
        self.assertIsNotNone(available_corners[2] in [0b100000000, 0b001000000, 0b000000001])