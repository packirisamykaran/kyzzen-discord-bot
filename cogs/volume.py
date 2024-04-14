# pylint: disable=import-error
from discord.ext import commands
from discord import app_commands
import discord
import aiohttp
from bot_config import stats_commands
from bot_config import get_collection_discord_config
from data.board_data import fetch_volume_data, get_sol_USD_price


class Volume(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Volume cog initialized.")
        # Dynamically add commands after initializing the cog
        # self.dynamic_commands = stats_commands

        # self.add_dynamic_commands()

    @app_commands.command(name='volume', description="Get volume data for the collection.")
    async def volume_stats(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        # Volume:
        # - Past 1H: x SOL  / x USD (+-x%)
        # - Past 24H: x SOL  / x USD (+-x%)
        # - Past 7D: x SOL  / x USD (+-x%)
        # - Past 30D: x SOL  / x USD (+-x%)

        guild_id = interaction.guild_id
        collection_config = get_collection_discord_config(guild_id)
        collection_id = collection_config["CollectionID"]

        # volumePast1h
        # volumePast24h
        # volumePast7d
        # volumePast30d
        # volumeTotal
        # volumePast1hDelta
        # volumePast24hDelta
        # volumePast7dDelta
        # volumePast30dDelta
        # volumeUsdPast1h
        # volumeUsdPast24h
        # volumeUsdPast7d
        # volumeUsdPast30d
        volume_stats = await fetch_volume_data(collection_id)

        if volume_stats:
            message = "**Volume Activity:**\n"

            def format_delta(delta):
                return f"🔺{delta}%" if delta > 0 else (f"🔻{-delta}%" if delta < 0 else "🔲 0%")

            message += f"Past 1H": {await self.format_values(volume_stats['volumePast1h'])} SOL({format_delta(float(volume_stats['volumePast1hDelta']))})\n"
            message += f"Past 24H: {await self.format_values(volume_stats['volumePast24h'])} SOL ({format_delta(float(volume_stats['volumePast24hDelta']))})\n"
            message += f"Past 7D: {await self.format_values(volume_stats['volumePast7d'])} SOL  ({format_delta(float(volume_stats['volumePast7dDelta']))})\n"
            message += f"Past 30D: {await self.format_values(volume_stats['volumePast30d'])} SOL / {await self.format_values(volume_stats['volumeUsdPast30d'])} USD ({format_delta(float(volume_stats['volumePast30dDelta']))})\n"
            await interaction.followup.send(message)

    async def format_values(self, value):
        num_value = float(value)
        if num_value >= 1000:
            num_value /= 1000
            return f"{num_value:.1f}K"
        return f"{num_value:.2f}"


async def setup(bot):
    await bot.add_cog(Volume(bot))
