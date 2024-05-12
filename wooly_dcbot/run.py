import os
from dotenv import load_dotenv
from discord import Intents, Client, Message

from wooly_dcbot.responses import get_response

# SET UP BOT
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

# MESSAGES
async def send_message(message: Message, message_txt: str):
    if not message_txt:
        print("empty message")
        return

    # only respond to messages that start with !
    if message_txt[0] == '!':
        message.content = message_txt[1:]
        try:
            response: str = get_response(message)
            await message.channel.send(response)
        except Exception as e:
            print(e)
    else:
        return


# STARTUP
@client.event
async def on_ready():
    print(f'{client.user} RUNNING')


# INCOMING MESSAGES
@client.event
async def on_message(message: Message):
    # don't reply to self
    if message.author == client.user:
        return

    username = str(message.author)
    message_text = str(message.content)
    channel = str(message.channel)

    print(f'[{channel}]-{username}: "{message_text}"')

    await send_message(message, message_text)

def run(token=''):
    if token == '':
        load_dotenv()
        token=os.getenv('DISCORD_TOKEN')
    client.run(token)

if __name__ == '__main__':
    run()
