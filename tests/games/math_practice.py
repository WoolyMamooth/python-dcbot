import unittest
from wooly_dcbot.games.math_practice import GameSession

class TestGameSession(unittest.TestCase):
    def setUp(self):
        self.session = GameSession()

    def test_next_question(self):
        for _ in range(20):
            question = self.session.next_question()
            self.assertTrue(isinstance(question, str))
            self.assertTrue(len(question) > 0)

    def test_check_answer(self):
        self.session.turn = 5
        self.session.next_question()
        self.assertTrue(self.session.check_answer(self.session.answer))
        self.assertFalse(self.session.check_answer(self.session.answer + 1))

if __name__ == '__main__':
    unittest.main()
