import wooly_dcbot.net.api
from wooly_dcbot.net.api import add_exp
from wooly_dcbot import utils

EXP_PER_WIN=100
HELP=("This is a simple game of hangman, I will think of a word and write as many _ s in chat as the word is long. "
      "You have to guess the word one letter at a time, but be careful, you can only make 7 mistakes, or you will be hanged. "
      "You can earn "+str(EXP_PER_WIN)+" exp for every letter in the word, but only if you win.")

sessions: dict = {}

class GameSession:
    def __init__(self):
        self.word, self.link= wooly_dcbot.net.api.hangman_get_word()
        self.shown_word=""
        for i in range(len(self.word)):
            self.shown_word += '_'
        self.wrong_guesses = 0
        self.new=True

    def ask_letter(self, letter):
        flag=False
        for i in range(0, len(self.word)):
            if self.word[i] == letter:
                temp=list(self.shown_word)
                temp[i]=letter
                self.shown_word ="".join(temp)
                flag=True
        if self.shown_word==self.word:
            return "Yes, the word was\n"+ utils.wrap_in_backtick(self.word)+ "\nYou win! Congrats!\n"+self.link
        if flag:
            return "Correct! " + utils.wrap_in_backtick(self.shown_word)

        self.wrong_guesses += 1
        if self.wrong_guesses >= 8:
            return draw_hangman(self.wrong_guesses)+"\nIt seems you lose this time. The word was:\n"+ utils.wrap_in_backtick(self.word)+ "\n"+self.link

        return draw_hangman(self.wrong_guesses)+"\nIncorrect.\n"+ utils.wrap_in_backtick(self.shown_word)


def draw_hangman(stage:int):
        drawing = ""
        if stage == 1:
            drawing = "|___"
        elif stage == 2:
            drawing = ("|\n"
                       "|\n"
                       "|\n"
                       "|___")
        elif stage == 3:
            drawing = ("|\n"
                       "|\n"
                       "|\n"
                       "|\n"
                       "|\n"
                       "|___")
        elif stage == 4:
            drawing = (",_______\n"
                       "|\n"
                       "|\n"
                       "|\n"
                       "|\n"
                       "|\n"
                       "|___")
        elif stage == 5:
            drawing = (",________\n"
                       "|       |\n"
                       "|       O\n"
                       "|\n"
                       "|\n"
                       "|\n"
                       "|___")
        elif stage == 6:
            drawing = (",________\n"
                       "|       |\n"
                       "|       O\n"
                       "|       |\n"
                       "|\n"
                       "|\n"
                       "|___\n")
        elif stage == 7:
            drawing = (",________\n"
                       "|       |\n"
                       "|       O\n"
                       "|      /|\\\n"
                       "|\n"
                       "|\n"
                       "|___")
        else:
            drawing = (",________\n"
                       "|       |\n"
                       "|       O\n"
                       "|      /|\\\n"
                       "|      / \\\n"
                       "|\n"
                       "|___")
        drawing = utils.wrap_in_backtick(drawing)
        return drawing

def new_session(user):
    sessions[user]=GameSession()

def has_user(user):
    return user in sessions.keys()

def responses(message, user):
    response=""
    if message == 'exit' or message == 'stop':
        response="Okay, let's do something else!"
        sessions.pop(user)
        return response
    else:
        if sessions[user].new:
            response="Let's begin:\n" + utils.wrap_in_backtick(sessions[user].shown_word)
            sessions[user].new=False
            return response

        if len(message) > 1:
            return "You can only guess one letter at a time."

        response=sessions[user].ask_letter(message)
        if "lose" in response:
            sessions.pop(user)
            return response
        elif "win" in response:
            if add_exp(user, 100*len(sessions[user].word)):
                response= utils.level_up_wrapper(response, user)
            sessions.pop(user)
            return response
        else:
            return response
