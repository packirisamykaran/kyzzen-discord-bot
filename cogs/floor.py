# pylint: disable=import-error
from discord.ext import commands
from discord import app_commands
import discord
import aiohttp
from data.board_data import fetch_floor_price_data
from bot_config import stats_group_commands, get_collection_discord_config
from data.board_data import get_sol_USD_price


class Floor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Dynamically add commands after initializing the cog
        # self.dynamic_commands = stats_commands

        # self.add_dynamic_commands()

    @app_commands.command(name='floor', description=stats_group_commands["stats-floor-price"]["description"])
    async def floor_price_stats(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        guild_id = interaction.guild_id
        collection_config = get_collection_discord_config(guild_id)
        collection_id = collection_config["CollectionID"]
        floor_price_stats = await fetch_floor_price_data(collection_id)
        sol_price = await get_sol_USD_price()

        floor_price = float(floor_price_stats['floorPrice'])
        deltas = {
            '1hr': float(floor_price_stats['floorPricePast1hDelta']),
            '24hr': float(floor_price_stats['floorPricePast24hDelta']),
            '7d': float(floor_price_stats['floorPricePast7dDelta']),
            # '30d': float(floor_price_stats['floorPricePast30dDelta'])
        }

        # Calculate and format floor price and changes
        message = await self.calculate_and_format_changes(floor_price, deltas, sol_price)
        await interaction.followup.send(message)

    async def calculate_and_format_changes(self, floor_price, deltas, sol_price):
        usd_value = floor_price * sol_price
        formatted_usd_value = await self.format_values(usd_value)
        current = f"🏷️ Floor Price: {floor_price:.2f} SOL | ${formatted_usd_value} USD\n"

        changes = "\n📉 Price Changes: \n"
        icons = {'1hr': '⏳', '24hr': '🕛', '7d': '🗓️', '30d': '🔄'}
        for period, delta in deltas.items():
            sol_change = floor_price / (1 + delta / 100)
            usd_change = sol_change * sol_price
            formatted_sol_change = await self.format_values(sol_change)
            formatted_usd_change = await self.format_values(usd_change)
            trend = "~" if delta == 0 else (
                f"🔻{-delta}%" if delta < 0 else f"🔺{delta}%")
            changes += f"{icons[period]} {period.upper()}: {formatted_sol_change} SOL | ${formatted_usd_change} USD ({trend})\n"

        return current + changes

    async def format_values(self, value):
        num_value = float(value)
        if num_value >= 1000:
            num_value /= 1000
            return f"{num_value:.1f}K"
        return f"{num_value:.2f}"
# ______________________________________________________________________________________________________________________

    # @app_commands.command(name='stats-sales', description=stats_group_commands["stats-sales"]["description"])
    # async def sales(self, interaction: discord.Interaction):

    #     await interaction.response.defer(ephemeral=True)

    #     guild_id = interaction.guild_id
    #     collection_config = get_collection_discord_config(guild_id)
    #     collection_id = collection_config["CollectionID"]
    #     sales_stats = await fetch_sales_data(collection_id)
    #     await interaction.followup.send(f"Sales 1H: {sales_stats['salesPast1h']}\nSales 24H: {sales_stats['salesPast24h']}\nSales 7D: {sales_stats['salesPast7d']}\nSales 30D: {sales_stats['salesPast30d']}")

    # @app_commands.command(name='stats-volume', description=stats_group_commands["stats-volume"]["description"])
    # async def volume(self, interaction: discord.Interaction):
    #     await interaction.response.defer(ephemeral=True)

    #     guild_id = interaction.guild_id
    #     collection_config = get_collection_discord_config(guild_id)
    #     collection_id = collection_config["CollectionID"]
    #     volume_stats = await fetch_volume_data(collection_id)
    #     await interaction.followup.send(f"Volume 1H: {volume_stats['volumePast1h']} SOL ({volume_stats['volumePast1hDelta']}%)\nVolume 24H: {volume_stats['volumePast24h']} SOL ({volume_stats['volumePast24hDelta']}%)\nVolume 7D: {volume_stats['volumePast7d']} SOL ({volume_stats['volumePast7dDelta']}%)\nVolume 30D: {volume_stats['volumePast30d']} SOL ({volume_stats['volumePast30dDelta']}%)\nTotal Volume: {volume_stats['volumeTotal']} SOL")

    # @app_commands.command(name='stats-usd-volume', description=stats_group_commands["stats-usd-volume"]["description"])
    # async def volume_usd(self, interaction: discord.Interaction):
    #     await interaction.response.defer(ephemeral=True)

    #     guild_id = interaction.guild_id
    #     collection_config = get_collection_discord_config(guild_id)
    #     collection_id = collection_config["CollectionID"]
    #     volume_usd_stats = await fetch_volume_usd_data(collection_id)
    #     await interaction.followup.send(f"Volume 1H: {volume_usd_stats['volumeUsdPast1h']} USD ({volume_usd_stats['volumePast1hDelta']}%)\nVolume 24H: {volume_usd_stats['volumeUsdPast24h']} USD ({volume_usd_stats['volumePast24hDelta']}%)\nVolume 7D: {volume_usd_stats['volumeUsdPast7d']} USD ({volume_usd_stats['volumePast7dDelta']}%)\nVolume 30D: {volume_usd_stats['volumeUsdPast30d']} USD ({volume_usd_stats['volumePast30dDelta']}%)")

    #


async def setup(bot):
    await bot.add_cog(Floor(bot))


# def add_dynamic_commands(self):
    #     for command in self.dynamic_commands:
    #         self.create_and_add_command(
    #             command["name"], command["description"], command["stat"], command["symbol"], command["response"])

    # def create_and_add_command(self, name, description, stat, symbol, response):
    #     @app_commands.command(name=name, description=description)
    #     async def dynamic_command(interaction: discord.Interaction):
    #         await interaction.response.defer(ephemeral=True)

    #         # get server id
    #         guild_id = interaction.guild_id

    #         # get collection id
    #         collection_config = get_collection_discord_config(guild_id)
    #         collection_id = collection_config["CollectionID"]

    #         # Example response, replace with your own logic
    #         responseStat = await fetch_stats(collection_id, stat)
    #         await interaction.followup.send(f"{response}: {responseStat} {symbol}")

    #     # Set `guild` if you want to restrict to a specific guild
    #     self.bot.tree.add_command(dynamic_command, guild=None)
