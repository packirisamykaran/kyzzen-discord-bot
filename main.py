# pylint: disable=import-error
# pylint: disable=redefined-outer-name
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

        # Initialize the command tree for application commands

        # Load extensions (cogs) upon bot initialization
        self.initial_extensions = [
            'cogs.board', "cogs.floor", "cogs.sales", "cogs.volume", "cogs.raffles"]

    async def setup_hook(self):
        # Load each extension from the list
        for extension in self.initial_extensions:
            try:
                await self.load_extension(extension)

                # Sync the application commands with Discord

            except commands.ExtensionError as e:
                print(f'Failed to load extension {extension}: {e}')
        await self.tree.sync()

    async def on_ready(self):
        # Notification that the bot is logged in and ready
        print(f'\nLogged in as {self.user} (ID: {self.user.id})\n')


# Initialize bot instance
bot = KyzzenBot(command_prefix='!', intents=intents)


# Run the bot
if __name__ == '__main__':
    try:
        bot.run(bot_key)
    except Exception as e:
        print(f'Error encountered: {e}')
