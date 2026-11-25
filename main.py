import os
from dotenv import load_dotenv
import copy
import logging
import discord
from discord.ext import commands
from discord import app_commands
from logger_config import setup_logging

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DEV_GUILD_ID = int(os.getenv('DEV_GUILD_ID'))
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True
GUILD_ID = discord.Object(id=DEV_GUILD_ID)

class Client(commands.Bot):
    async def setup_hook(self):
        logger.info("Starting command sync...")
        await self.tree.sync(guild=GUILD_ID)
        logger.info(f"Synced commands to guild {DEV_GUILD_ID}")
    async def on_ready(self):
        logger.info(f'Logged in as {self.user}')

client = Client(command_prefix='!', intents=intents)

@client.tree.command(name='hello', description='Say Hello', guild=GUILD_ID)
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello there!")

if __name__ == '__main__':
    setup_logging(level=logging.INFO)
    client.run(BOT_TOKEN, log_handler=None)