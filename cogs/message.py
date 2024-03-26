from discord.ext import commands
from discord import app_commands
import discord


class MessageCommands(commands.Cog):
    """
    A cog for simple message-based commands.
    This cog includes commands for greeting and farewells.
    """

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def hello(self, interaction: discord.Interaction):
        """
        Responds with a greeting message.
        """
        await interaction.response.send_message('Hello! How are you today?')

    @app_commands.command()
    async def bye(self, interaction: discord.Interaction):
        """
        Responds with a greeting message.
        """
        await interaction.response.send_message('Hebye')


async def setup(bot):
    """
    The setup function to add this cog to a bot.
    """
    await bot.add_cog(MessageCommands(bot))
