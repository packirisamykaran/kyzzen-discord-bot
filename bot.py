import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio


# Load environment variables from .env file
load_dotenv()
bot_key = os.getenv('BOT_KEY')
# Congfigs

# Define intents
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True


# Initialize the bot with intents
bot = commands.Bot(command_prefix='/', intents=intents)

asyncio.run(bot.load_extension('cogs.board'))
asyncio.run(bot.load_extension('cogs.message'))


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


if __name__ == '__main__':
    bot.run(bot_key)
