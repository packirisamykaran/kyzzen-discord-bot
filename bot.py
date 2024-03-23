import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
bot_key = os.getenv('BOT_KEY')

# Define discord intents for more granular control over events the bot listens to
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True


class KyzzenBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

        # Load extensions (cogs) upon bot initialization
        self.initial_extensions = ['cogs.board', 'cogs.message']

    async def setup_hook(self):
        # Load each extension from the list
        for extension in self.initial_extensions:
            try:
                await self.load_extension(extension)
            except commands.ExtensionError as e:
                print(f'Failed to load extension {extension}: {e}')

    async def on_ready(self):
        # Notification that the bot is logged in and ready
        print(f'Logged in as {self.user} (ID: {self.user.id})')


# Initialize bot instance
bot = KyzzenBot(command_prefix='/', intents=intents)

# Run the bot
if __name__ == '__main__':
    try:
        bot.run(bot_key)
    except Exception as e:
        print(f'Error encountered: {e}')
