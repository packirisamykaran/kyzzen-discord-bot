# pylint: disable=import-error
import discord
from discord.ext import commands
from data.board_data import fetch_loan_offers
from bot_config import get_collection_discord_config
from discord import app_commands


class Loans(commands.Cog):
    """Discord bot cog for managing NFT loans."""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='loanofferhighest', description="Get highest loan offer for the collection.")
    async def loan_stats(self, interaction: discord.Interaction):
        # {'highest_offer': '120.03 SOL', 'apy': '180.00%', 'duration': '7 Days', 'marketplace': 'Sharky'}

        await interaction.response.defer(ephemeral=True)

        guild_id = interaction.guild_id
        collection_config = get_collection_discord_config(guild_id)
        collection_id = collection_config["CollectionID"]

        loan_stats = await fetch_loan_offers("Mad Lads")

        message = f"Highest Loan Offer: {loan_stats['highest_offer']}\n"
        message += f"Borrower Interest: {loan_stats['apy']}\n"
        message += f"Duration: {loan_stats['duration']}\n"
        message += f"Borrow Now: <{loan_stats['link']}>\n"

        await interaction.followup.send(message)


async def setup(bot):
    await bot.add_cog(Loans(bot))
