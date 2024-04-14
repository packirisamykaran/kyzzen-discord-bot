# pylint: disable=import-error
from discord.ext import commands
from discord import app_commands
import discord
import aiohttp

from bot_config import get_collection_discord_config
from data.board_data import fetch_raffles
from utils import lamport_to_sol


class Raffles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Raffles cog initialized.")
        # Dynamically add commands after initializing the cog
        # self.dynamic_commands = stats_commands

        # self.add_dynamic_commands()

    @app_commands.command(name='raffles', description="Get raffle data for the collection.")
    async def raffle_stats(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        guild_id = interaction.guild_id
        collection_config = get_collection_discord_config(guild_id)
        collection_id = collection_config["CollectionID"]

        raffle_stats = await fetch_raffles(collection_id)

        # Raffle 1: (nft name)
        # Rarity Rank: MoonRank x / HowRare x
        # Ending: (date/time remaining)
        # Price/Ticket: x SOL
        # Tickets Remaining: x / x
        # Link:

        if raffle_stats:
            message = f"**Ongoing Raffles:{len(raffle_stats)}**\n"
            message += f"Raffle 1: {raffle_stats['name']}\n"
            message += f"Rarity Rank: MoonRank {raffle_stats['moonrankRank']} / howRareRang {raffle_stats['howRareRank']}\n"
            message += f"Ending: {raffle_stats['endData'].split('T')[0]}\n"
            message += f"Price/Ticket: {lamport_to_sol(raffle_stats['price'])} SOL\n"
            message += f"Tickets Remaining: {raffle_stats['supply']-raffle_stats['sold']} / {raffle_stats['supply']}\n"
            message += f"Link: [View Raffle]({raffle_stats['creators'][0]})\n"

            await interaction.followup.send(message)
        else:
            await interaction.followup.send("No ongoing raffles currently.")


async def setup(bot):
    await bot.add_cog(Raffles(bot))
