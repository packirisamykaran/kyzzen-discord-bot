# pylint: disable=import-error
from discord.ext import commands
from discord import app_commands
import discord
from bot_config import stats_commands
from data.board_data import fetch_stats, fetch_sales_data, fetch_volume_data, fetch_volume_usd_data, fetch_floor_price_data
from bot_config import stats_group_commands, get_collection_discord_config


class StatsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Dynamically add commands after initializing the cog
        self.dynamic_commands = stats_commands

        self.add_dynamic_commands()

    @app_commands.command(name='stats-sales', description=stats_group_commands["stats-sales"]["description"])
    async def sales(self, interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)

        guild_id = interaction.guild_id
        collection_config = get_collection_discord_config(guild_id)
        collection_id = collection_config["CollectionID"]
        sales_stats = await fetch_sales_data(collection_id)
        await interaction.followup.send(f"Sales 1H: {sales_stats['salesPast1h']}\nSales 24H: {sales_stats['salesPast24h']}\nSales 7D: {sales_stats['salesPast7d']}\nSales 30D: {sales_stats['salesPast30d']}")

    @app_commands.command(name='stats-volume', description=stats_group_commands["stats-volume"]["description"])
    async def volume(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        guild_id = interaction.guild_id
        collection_config = get_collection_discord_config(guild_id)
        collection_id = collection_config["CollectionID"]
        volume_stats = await fetch_volume_data(collection_id)
        await interaction.followup.send(f"Volume 1H: {volume_stats['volumePast1h']} SOL ({volume_stats['volumePast1hDelta']}%)\nVolume 24H: {volume_stats['volumePast24h']} SOL ({volume_stats['volumePast24hDelta']}%)\nVolume 7D: {volume_stats['volumePast7d']} SOL ({volume_stats['volumePast7dDelta']}%)\nVolume 30D: {volume_stats['volumePast30d']} SOL ({volume_stats['volumePast30dDelta']}%)\nTotal Volume: {volume_stats['volumeTotal']} SOL")

    @app_commands.command(name='stats-floor-price', description=stats_group_commands["stats-floor-price"]["description"])
    async def floor_price_stats(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        guild_id = interaction.guild_id
        collection_config = get_collection_discord_config(guild_id)
        collection_id = collection_config["CollectionID"]
        floor_price_stats = await fetch_floor_price_data(collection_id)
        await interaction.followup.send(f"Floor Price: {floor_price_stats['floorPrice']} SOL\nFloor Price 1H Change: {floor_price_stats['floorPricePast1hDelta']}%\nFloor Price 24H Change: {floor_price_stats['floorPricePast24hDelta']}%\nFloor Price 7D Change: {floor_price_stats['floorPricePast7dDelta']}%\nFloor Price 30D Change: {floor_price_stats['floorPricePast30dDelta']}%")

    @app_commands.command(name='stats-usd-volume', description=stats_group_commands["stats-usd-volume"]["description"])
    async def volume_usd(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        guild_id = interaction.guild_id
        collection_config = get_collection_discord_config(guild_id)
        collection_id = collection_config["CollectionID"]
        volume_usd_stats = await fetch_volume_usd_data(collection_id)
        await interaction.followup.send(f"Volume 1H: {volume_usd_stats['volumeUsdPast1h']} USD ({volume_usd_stats['volumePast1hDelta']}%)\nVolume 24H: {volume_usd_stats['volumeUsdPast24h']} USD ({volume_usd_stats['volumePast24hDelta']}%)\nVolume 7D: {volume_usd_stats['volumeUsdPast7d']} USD ({volume_usd_stats['volumePast7dDelta']}%)\nVolume 30D: {volume_usd_stats['volumeUsdPast30d']} USD ({volume_usd_stats['volumePast30dDelta']}%)")

    def add_dynamic_commands(self):
        for command in self.dynamic_commands:
            self.create_and_add_command(
                command["name"], command["description"], command["stat"], command["symbol"], command["response"])

    def create_and_add_command(self, name, description, stat, symbol, response):
        @app_commands.command(name=name, description=description)
        async def dynamic_command(interaction: discord.Interaction):
            await interaction.response.defer(ephemeral=True)

            # get server id
            guild_id = interaction.guild_id

            # get collection id
            collection_config = get_collection_discord_config(guild_id)
            collection_id = collection_config["CollectionID"]

            # Example response, replace with your own logic
            responseStat = await fetch_stats(collection_id, stat)
            await interaction.followup.send(f"{response}: {responseStat} {symbol}")

        # Set `guild` if you want to restrict to a specific guild
        self.bot.tree.add_command(dynamic_command, guild=None)


async def setup(bot):
    await bot.add_cog(StatsCommands(bot))
