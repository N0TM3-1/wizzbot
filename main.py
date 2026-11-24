import os
from dotenv import load_dotenv
import logging
import discord
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
logger = logging.getLogger(__name__)

class Client(discord.Client):
    async def on_ready(self):
        logger.debug(f'Logged in as {self.user}')

intents = discord.Intents.default()
intents.message_content = True

if __name__== '__main__':
    logging.basicConfig(filename='log.log', level=logging.DEBUG)

    client = Client(intents=intents)
    client.run(BOT_TOKEN)