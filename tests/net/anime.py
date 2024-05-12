import unittest
from unittest.mock import patch
from wooly_dcbot.net.anime import Anime, update_list, get_random, animes


class TestAnime(unittest.TestCase):
    @patch('wooly_dcbot.net.anime.webdriver.Chrome')
    @patch('wooly_dcbot.net.anime.webdriver.ChromeOptions')
    @patch('wooly_dcbot.net.anime.bs4.BeautifulSoup')
    def test_update_list(self, mock_BeautifulSoup, mock_ChromeOptions, mock_Chrome):
        mock_driver = mock_Chrome.return_value
        mock_driver.get.return_value = None
        mock_soup = mock_BeautifulSoup.return_value
        mock_titles = [mock_title('Title1', 'Link1'), mock_title('Title2', 'Link2')]
        mock_soup.find_all.return_value = mock_titles
        update_list()
        self.assertEqual(len(animes), 2)

    @patch('wooly_dcbot.net.anime.random.choice')
    def test_get_random(self, mock_choice):
        mock_anime = Anime('Mock Anime', '9', 'https://example.com')
        mock_choice.return_value = mock_anime
        result = get_random()
        self.assertEqual(result, mock_anime)

def mock_title(title, link):
    mock_title = unittest.mock.Mock()
    mock_title.get_text.return_value = title
    mock_title.get.return_value = link
    return mock_title

if __name__ == '__main__':
    unittest.main()
