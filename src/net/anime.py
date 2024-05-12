import os
import random

import bs4
from selenium import webdriver

from src import utils

HELP=("If you use the " + utils.bold("!anime") + " command, I will recommend you an anime based on the MAL page of"
      " my creator. You can also use " + utils.bold("!anime update") +
      " in which case I will check his page and update the list in my memory.")


animes:list=[]

class Anime:
    def __init__(self,title,score,link):
        self.title=title
        self.score=score
        self.link=link

def update_list():
    """
    Updates the list of animes stored in memory by accessing a MAL page through Selenium.
    :return:
    """
    url=os.getenv("ANIME_URL")
    animes.clear()

    #--headless option makes it not open a window
    options=webdriver.ChromeOptions()
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    html=driver.page_source
    soup=bs4.BeautifulSoup(html, "html.parser")
    titles=soup.find_all("a",attrs={"class":"link sort"})
    titles=titles[4:]
    titles=titles[1::2]

    scores=soup.find_all("span",attrs={"class":"score-label"})
    scores=scores[1:]

    i=0
    for title in titles:
        if int(scores[i].get_text()) < 8:
            break
        animes.append(Anime(title.get_text(),scores[i].get_text().strip(),"https://myanimelist.net/"+title.get('href')))
        i+=1

    driver.close()

def get_random():
    """
    Returns a random Anime object from the list.
    :return:
    """
    #update our anime list only when needed
    if not animes:
        print("UPDATING ANIME LIST")
        update_list()
    return random.choice(animes)

