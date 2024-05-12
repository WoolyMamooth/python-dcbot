import unittest
from wooly_dcbot.games.tictactoe import GameSession, check_win

class TestGameSession(unittest.TestCase):
    def setUp(self):
        self.session = GameSession("test_user")

    def test_initial_state(self):
        # Test if the initial state is set up correctly
        self.assertEqual(self.session.get_username, "test_user")
        self.assertEqual(self.session.get_board, [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])

    def test_next_turn(self):
        # Test if next_turn method updates the board correctly
        self.assertEqual(self.session.next_turn(1), "-")  # Assuming placing X in first position is valid
        self.assertEqual(self.session.get_board, ['X', 'O', ' ', ' ', ' ', ' ', ' ', ' ', ' '])  # Board should be updated
        # Test if next_turn method handles invalid moves
        self.assertEqual(self.session.next_turn(1), "There's already an X there.")  # Trying to place X again in same position

    def test_check_win(self):
        # Test if check_win method correctly identifies winning scenarios
        self.session._board = ['X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ']  # Horizontal win
        self.assertEqual(check_win(self.session, 'X'), 'X')
        self.session._board = ['O', ' ', ' ', 'O', ' ', ' ', 'O', ' ', ' ']  # Diagonal win
        self.assertEqual(check_win(self.session, 'O'), 'O')
        # Test if check_win method correctly identifies draw scenarios
        self.session._board = ['X', 'O', 'X', 'X', 'O', 'O', 'O', 'X', 'X']  # Draw scenario
        self.assertEqual(check_win(self.session, 'X'), 'D')

    def test_board_to_string(self):
        # Test if board_to_string method returns the board in the correct format
        expected_board = (
            "```  |   |  \n"
            "----------\n"
            "  |   |  \n"
            "----------\n"
            "  |   |  \n```"
        )
        self.assertEqual(self.session.board_to_string(), expected_board)

if __name__ == '__main__':
    unittest.main()
