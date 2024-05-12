from discord import Message

from net import api, anime
from games import tictactoe, math_practice, hangman
import utils

commands:list=["help","tictac","hangman","math","anime","level"]
def get_response(user_message: Message) -> str:
    lowered = user_message.content.lower()
    user = str(user_message.author)

    # handles games
    if tictactoe.has_user(user):
        return tictactoe.responses(lowered, user)

    if math_practice.has_user(user):
        return math_practice.responses(lowered,user)

    if hangman.has_user(user):
        return hangman.responses(lowered,user)

    # handles general interaction
    if lowered == '':
        return "How can I help?"
    elif 'test' in lowered:
        return "Working."

    elif 'help' in lowered:
        if 'tic' in lowered or 'tac' in lowered:
            return tictactoe.HELP
        if 'math' in lowered:
            return math_practice.HELP
        if 'hang' in lowered:
            return hangman.HELP
        if 'anime' in lowered:
            return anime.HELP
        if 'level' in lowered:
            if 'help' in lowered:
                return ("You can earn exp by playing games with me, for every 1000 exp you go up 1 level. "
                        "You can check your level by using the " + utils.bold("!level") + " command."
                        " Levels don't mean much, but you can show it off to your friends.")

        response="List of commands:\n"
        for c in commands:
            response+=f'\t!{c}\n'
        response+=("You can also add "+utils.italic("help")+" after any other command to learn more about it. "
                   "Please remember that I only pay attention to messages starting with a ! character, even if "
                   "your message is just a number, or a letter. Have fun!")
        return response

    #GAMES
    elif 'tic' in lowered or 'tac' in lowered:
        tictactoe.new_session(user)
        return "Let's play Tic-Tac-Toe! You go first:\n" + tictactoe.get_session(user)

    elif 'math' in lowered:
        math_practice.new_session(user)
        return math_practice.responses(lowered,user)

    elif 'hang' in lowered:
        hangman.new_session(user)
        return hangman.responses(lowered,user)

    #OTHER
    elif 'anime' in lowered:
        if 'update' in lowered:
            anime.update_list()
            return "Okay, I updated the list."
        a=anime.get_random()
        return "I would recommend watching "+a.title+" if you havent seen it. A man of great taste gave it a score of "+a.score+"/10.\n"+a.link

    elif 'level' in lowered:
        return "You are level "+utils.bold(api.whats_my_level(user))+ "! You can level up by playing games."
    else:
        return "Unkown command, please use "+utils.bold("!help")+" for more information!"
