import discord
from discord.ext import commands
import requests

# Define intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Ensure you enable message content intent

# Initialize the bot with intents
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Define the command to respond to "!hi"


@bot.command(name='hi')  # Update the command name to 'hi'
async def hi(ctx):
    await ctx.send('hi')  # Update the response to 'hi'


# Replace 'YOUR_BOT_TOKEN' with your bot's actual token
bot.run('MTIxODQ5NjM0MDk1NTM2NTM4Ng.GOjJs9.SI9tYB5BrCXbTw-oQYLUl2iSCqwX7Q5XJS5cK4')
