import random

from wooly_dcbot import utils
from wooly_dcbot.net.api import add_exp

EXP_PER_WIN=100
HELP=("This is a game designed to help you practice math. "
      "I will ask you increasingly difficult math questions, addition, subtraction or multiplication. "
      "We go as long as you can answer them, once you give a wrong answer, you lose. "
      "You can earn "+str(EXP_PER_WIN)+" exp for every correct answer.")

sessions:dict={}

"""
Gives the player increasingly difficult math questions as long as they can answer.
"""
class GameSession:
    def __init__(self):
        self.turn=0
        self.answer=0

    def next_question(self):
        num1="1"
        num2="1"

        difficulty=self.turn // 5
        if difficulty == 0:
            num1=random.randint(1,10)
            num2=random.randint(1,10)
        elif difficulty == 1:
            num1=random.randint(1,10)
            num2=random.randint(1,100)
        elif difficulty == 2:
            num1=random.randint(1,100)
            num2=random.randint(1,100)
        elif difficulty == 3:
            num1=random.randint(1,10)
            num2=random.randint(1,1000)
        elif difficulty == 4:
            num1=random.randint(1,100)
            num2=random.randint(1,1000)
        elif difficulty == 5:
            num1=random.randint(1,1000)
            num2=random.randint(1,1000)
        else:
            num1=random.randint(1,10000)
            num2=random.randint(1,10000)

        operation=random.choice(["+","-","*"])

        if operation=='+':
            self.answer= num1 + num2
        elif operation=='-':
            if num1<num2:
                temp=num1
                num1=num2
                num2=temp
            self.answer= num1 - num2
        elif operation=="*":
            self.answer= num1 * num2

        question=f'{num1}{operation}{num2}'

        self.turn+=1
        return question

    def check_answer(self,answer:int):
        print("Checking: " + str(answer) +" == " + str(self.answer))
        return answer==self.answer

def new_session(user):
    sessions[user]=GameSession()

def get_session(user):
    pass

def has_user(user):
    return user in sessions.keys()

def responses(message,user):
    response=""
    if message == 'exit' or message == 'stop':
        response="Okay, let's do something else!"
        if add_exp(user,EXP_PER_WIN*sessions[user].turn):
            response= utils.level_up_wrapper(response, user)
        sessions.pop(user)
    else:
        if sessions[user].turn!=0:
            if sessions[user].check_answer(int(message.strip())):
                response+=(random.choice(['Correct!','Very good!','Awesome!','Fantastic!','Good job!'])
                           +" "
                           +random.choice(['Next up:','Next question:','How about:'])
                           +" "
                           +sessions[user].next_question()+" = ?"
                           )
            else:
                response+=(random.choice(["Sadly that's incorrect.","Sadly, no.","Unfortunately, no."])
                           +" The correct answer was " + str(sessions[user].answer) + ". Better luck next time")
                if add_exp(user,EXP_PER_WIN*sessions[user].turn):
                    response= utils.level_up_wrapper(response, user)
                sessions.pop(user)
        else:
            response+=random.choice(['Lets start!'])+" What is "+sessions[user].next_question()+" ?"
    return response


if __name__=="__main__":
    new_session("Wooly")