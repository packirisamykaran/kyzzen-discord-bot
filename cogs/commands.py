# pylint: disable=import-error
from discord.ext import commands
from discord import app_commands
import discord
from admin_database import stats_commands
from data.board_data import fetchStats
from config import CollectionID


class StatsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Dynamically add commands after initializing the cog
        self.dynamic_commands = stats_commands

        self.add_dynamic_commands()

    def add_dynamic_commands(self):
        for command in self.dynamic_commands:
            self.create_and_add_command(
                command["name"], command["description"], command["stat"], command["symbol"], command["response"])

    def create_and_add_command(self, name, description, stat, symbol, response):
        @app_commands.command(name=name, description=description)
        async def dynamic_command(interaction: discord.Interaction):
            # Example response, replace with your own logic
            responseStat = await fetchStats(CollectionID, stat)
            await interaction.response.send_message(f"{response}: {responseStat} {symbol}")

        # Set `guild` if you want to restrict to a specific guild
        self.bot.tree.add_command(dynamic_command, guild=None)


async def setup(bot):
    await bot.add_cog(StatsCommands(bot))
