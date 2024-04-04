# import discord
# pylint: disable=import-error
from discord import app_commands
from discord.ext import commands
import discord
from board_data import fetchStats

# Slash commands for stats


class StatsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Get NFT Floor Price")
    async def floor_price(self, interaction: discord.Interaction):
        floor_price = await fetchStats("0e8e33630d554702a1619418269808b4", "floorPrice")
        formatted_floor_price = floor_price / 10**9

        await interaction.response.send_message(f"Floor Price: {formatted_floor_price:.2f} SOl")


async def setup(bot):
    await bot.add_cog(StatsCommands(bot))
