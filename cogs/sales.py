# pylint: disable=import-error
import discord
from data.board_data import fetch_sales_data
from discord import app_commands
from discord.ext import commands
from bot_config import get_collection_discord_config


class Sales(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Sales cog initialized.")

    @app_commands.command(name='sales', description="Get sales data for the collection.")
    async def sales_data(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        guild_id = interaction.guild_id
        collection_config = get_collection_discord_config(guild_id)
        collection_id = collection_config["CollectionID"]

        sales_data = await fetch_sales_data(collection_id)
        if sales_data:
            message = "**Sales Activity:**\n"
            message += f"⏳ Hour: {sales_data['salesPast1h']}\n"
            message += f"🕛 24 Hours: {sales_data['salesPast24h']}\n"
            message += f"📅 Week: {sales_data['salesPast7d']}\n"
            message += f"🗓️ Month: {sales_data['salesPast30d']}\n"
            await interaction.followup.send(message)


async def setup(bot):
    await bot.add_cog(Sales(bot))
