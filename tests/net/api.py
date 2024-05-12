import unittest
from unittest.mock import patch, Mock
from src.net.api import whats_my_level, add_exp, hangman_get_word

class TestAPIFunctions(unittest.TestCase):

    @patch('src.net.api.requests.post')
    def test_whats_my_level(self, mock_post):
        mock_response = Mock()
        mock_response.text = '5'
        mock_post.return_value = mock_response

        level = whats_my_level('test_user')

        self.assertEqual(level, '5')

    @patch('src.net.api.requests.post')
    def test_add_exp(self, mock_post):
        mock_response = Mock()
        mock_response.text = 'levelup'
        mock_post.return_value = mock_response

        level_up = add_exp('test_user', 100)

        self.assertTrue(level_up)

    @patch('src.net.api.requests.get')
    def test_hangman_get_word(self, mock_get):
        mock_response = Mock()
        mock_response.url = 'https://wordnik.com/randoml?random=true'
        mock_get.return_value = mock_response

        word, url = hangman_get_word()

        self.assertEqual(word, 'wordnik.com')
        self.assertEqual(url, 'https://wordnik.com/randoml')
