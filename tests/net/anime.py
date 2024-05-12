import unittest
from unittest.mock import patch
from src.net.anime import Anime, update_list, get_random, animes


class TestAnime(unittest.TestCase):
    @patch('src.net.anime.webdriver.Chrome')
    @patch('src.net.anime.webdriver.ChromeOptions')
    @patch('src.net.anime.bs4.BeautifulSoup')
    def test_update_list(self, mock_BeautifulSoup, mock_ChromeOptions, mock_Chrome):
        mock_driver = mock_Chrome.return_value
        mock_driver.get.return_value = None
        mock_soup = mock_BeautifulSoup.return_value
        mock_titles = [mock_title('Title1', 'Link1'), mock_title('Title2', 'Link2')]
        mock_soup.find_all.return_value = mock_titles
        update_list()
        self.assertEqual(len(animes), 2)

    @patch('src.net.anime.random.choice')
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
