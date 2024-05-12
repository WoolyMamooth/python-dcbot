from src.net import api


def wrap_in_backtick(string:str)->str:
    """
    Wraps the given string in triple backticks, which signifies to Discord that it is meant to be code.
    Makes some messages look better.
    :param string:
    :return:
    """
    return "```"+string+"```"

def bold(string:str):
    """
    A text passed through this function will appear in bold on Discord.
    :param string:
    :return:
    """
    return f'**{string}**'

def italic(string:str):
    """
    A text passed through this function will appear in italic on Discord.
    :param string:
    :return:
    """
    return f'*{string}*'

def level_up_wrapper(message, user):
    """
    Adds an extra line to the message which shows the users level.
    :param message:
    :param user:
    :return:
    """
    return message+"\n"+italic("You levelled up!")+" You are now level "+bold(api.whats_my_level(user))+ "!"
