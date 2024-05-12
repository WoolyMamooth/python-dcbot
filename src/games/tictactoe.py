from src import utils
from src.net import api
from src.utils import wrap_in_backtick, bold

PLAYER_CHAR= 'X'
BOT_CHAR= 'O'
EXP_PER_WIN=1000
HELP=("The rules of Tic-Tac-Toe are very simple. You will play as X and I will play as O."
            " I will display a 3 by 3 grid, all you have to do is tell me which square"
            " you want to put your X. We will refer to the squares by their number, like this:\n" +
      wrap_in_backtick("1 | 2 | 3\n----------\n4 | 5 | 6\n----------\n7 | 8 | 9") +
            "So for example if you want to put an X on square 6, you just say **!6** and I "
            "will write it there if it isn't already occupied. You win by placing 3 Xs next to each other,"
            " either in a row, in a column or diagonally. If you want to play, just use the command " +
      bold("!tictac") +". You can get "+str(EXP_PER_WIN)+" exp for every win, and half of it for a draw.")

class GameSession:
    """
    Uses the opponents Discord username as an identifier, keeps the game in memory until someone wins.
    Player is X, bot is O.
    """

    def __init__(self, username: str):
        self._username = username
        self._current_player = PLAYER_CHAR
        self._board = [" " for i in range(9)]

    def next_turn(self, message: int) -> str:
        """
        Returns '-' if the players turn was successfully completed,
        a message otherwise.
        :param message: an int from 1 to 9, where the player wants to place their X
        :return:
        """
        if 0 < message < 10:
            message -= 1
            if self._board[message] == ' ':
                self._board[message] = PLAYER_CHAR  # player steps
                state=check_win(self, PLAYER_CHAR)
                if state != '-':
                    return state

                self._board = predict(self._board)  # bot steps
                state=check_win(self, BOT_CHAR)
                return state
            else:
                return "There's already an " + self._board[message] + " there."
        else:
            return ("There are only 9 places on the board. We count them from the top left to the bottom right, "
                    "starting at 1 and ending at 9")

    def board_to_string(self) -> str:
        response = (self._board[0] + " | " + self._board[1] + " | " + self._board[2] + "\n")
        response += "----------\n"
        response += (self._board[3] + " | " + self._board[4] + " | " + self._board[5] + "\n")
        response += "----------\n"
        response += (self._board[6] + " | " + self._board[7] + " | " + self._board[8] + "\n")
        response=wrap_in_backtick(response)
        return response

    @property
    def get_username(self):
        return self._username

    @property
    def get_board(self):
        return self._board


def predict(board):
    """
    The bot plays its turn and returns the new board state.
    :param board:
    """
    for i in range(9):
        if board[i] == " ":
            board[i] = BOT_CHAR
            return board
    return board


def check_win(session: GameSession, char):
    """
    Returns who the winner is(X or O), - if noone has won yet and D if it's a draw.
    :param char: player to check for
    :param session:
    :return:
    """
    board=session.get_board

    #check rows
    for i in [0,3,6]:
        if board[i] == char and board[i+1] == char and board[i+2] == char:
            return char
    #check columns
    for i in range(3):
        if board[i] == char and board[i+3] == char and board[i+6] == char:
            return char
    #check diagonals
    if board[0] == char and board[4] == char and board[8] == char:
        return char
    if board[2] == char and board[4] == char and board[6] == char:
        return char

    #check draw
    if " " not in board:
        return 'D'

    return '-'

ttt_sessions: dict = {}

def new_session(user):
    ttt_sessions[user] = (GameSession(user))

def get_session(user):
    return ttt_sessions[user].board_to_string()

def has_user(user):
    return (user in ttt_sessions.keys())

def responses(message, user):
    if message == 'exit' or message == 'stop':
        ttt_sessions.pop(user)
        return "Okay, let's do something else!"
    else:
        response = ttt_sessions[user].next_turn(int(message))
        if response == '-':
            return ttt_sessions[user].board_to_string()
        elif response == "D":
            response = ttt_sessions[user].board_to_string() + "\nIt's a draw!"
            if api.add_exp(user, EXP_PER_WIN * 0.5):
                response= utils.level_up_wrapper(response, user)
            ttt_sessions.pop(user)
            return response
        elif response == PLAYER_CHAR:
            response = ttt_sessions[user].board_to_string() + "\nYou win! Good job! :D"
            if api.add_exp(user, EXP_PER_WIN):
                response= utils.level_up_wrapper(response, user)
            ttt_sessions.pop(user)
            return response
        elif response == BOT_CHAR:
            response = ttt_sessions[user].board_to_string() + "\nLooks like I won this one. Wanna go again?"
            ttt_sessions.pop(user)
            return response
        else:
            return response
