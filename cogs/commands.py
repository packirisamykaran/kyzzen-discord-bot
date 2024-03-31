# import discord
from discord import app_commands
from data.board_data import fetchFloorPrice
from discord.ext import commands
import discord

# Slash commands for stats


class StatsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="floorprice")
    async def floorprice(self, ctx):
        floor_price = await fetchFloorPrice()
        formatted_floor_price = floor_price / 10**9

        await ctx.send(f"Floor Price: {formatted_floor_price:.2f} SOl")

    @app_commands.command(description="Get NFT Floor Price")
    async def floor_price(self, interaction: discord.Interaction):
        floor_price = await fetchFloorPrice()
        formatted_floor_price = floor_price / 10**9

        await interaction.response.send_message(f"Floor Price: {formatted_floor_price:.2f} SOl")


async def setup(bot):
    await bot.add_cog(StatsCommands(bot))
