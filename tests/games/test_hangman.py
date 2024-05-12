import unittest
import src.games.hangman as hangman

class TestHangman(unittest.TestCase):
    def setUp(self):
        self.user = "test_user"
        self.mock_game_session = hangman.GameSession()

    def test_ask_letter_correct_guess(self):
        self.mock_game_session.word = "hangman"
        self.mock_game_session.shown_word = "_______"
        response = self.mock_game_session.ask_letter("a")
        self.assertEqual(response, "Correct! ```_a___a_```")

    def test_ask_letter_lose(self):
        self.mock_game_session.word = "hangman"
        self.mock_game_session.shown_word = "_______"
        self.mock_game_session.wrong_guesses = 7
        response = self.mock_game_session.ask_letter("z")
        self.assertTrue("lose" in response)


if __name__ == "__main__":
    unittest.main()
