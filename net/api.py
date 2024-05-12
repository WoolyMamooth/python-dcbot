import os

import requests

def whats_my_level(username):
    """
    Sends a post request to the api url with the following data:

    {"whatsmylevel": True, "username": username}

    It expects a single int as response which represents the level of the user.
    :param username:
    :return:
    """
    url = os.getenv("API_URL")
    data = {
        "whatsmylevel": True,
        "username": username
    }

    response = requests.post(url, data=data)
    print(response.text)
    return response.text

def add_exp(username,exp):
    """
    Sends a post request to the api url with the following data:

    {"addexp": True, "username": username, "exp": exp}

    It returns True if the user levelled up.
    :param username:
    :return:
    """
    url = os.getenv("API_URL")
    data = {
        "addexp": True,
        "username": username,
        "exp": exp
    }

    response = requests.post(url, data=data)
    print(response.text)
    if response.text == "levelup":
        return True

def hangman_get_word():
    url = "https://wordnik.com/randoml"
    response = requests.get(url, allow_redirects=True)
    redirected_url = response.url
    print("Redirected URL:", redirected_url)
    word=redirected_url.split("/")[-2]
    print(word)
    return word.replace('%20',' '),redirected_url.replace('?random=true','')

