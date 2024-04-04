# pylint: disable=import-error
from discord.ext import commands, tasks
import discord
from data.board_data import fetch_board_data
from admin_database import get_collection_discord_data, statistic_channel_names, statistic_channel_names_reverse


class Board(commands.Cog):
    """Discord bot cog for managing NFT data boards."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Event listener for when the bot is ready."""
        if not self.update_nft_data.is_running():
            self.update_nft_data.start()

    @tasks.loop(hours=2)
    async def update_nft_data(self):
        """Task loop to update NFT data."""
        for guild in self.bot.guilds:
            await self.update_server_nft_data(guild)

    @update_nft_data.before_loop
    async def before_update_nft_data(self):
        """Ensures the bot is ready before starting the task loop."""
        await self.bot.wait_until_ready()

    async def update_server_nft_data(self, guild):
        """Updates NFT data for a single server."""
        server_config = await self.get_server_config(guild.id)
        if not server_config:
            return  # Server configuration not found or incomplete

        board_data = await fetch_board_data()
        await self.manage_voice_channels(guild, server_config, board_data)

    async def get_server_config(self, serverID):
        """Fetches and validates server configuration."""
        collection_server_config = get_collection_discord_data(serverID)
        if collection_server_config is None or 'board' not in collection_server_config or 'categoryID' not in collection_server_config:
            print(
                f"Server configuration incomplete or not found for server: {serverID}")
            return None
        return collection_server_config

    async def manage_voice_channels(self, guild, server_config, board_data):
        """Creates or updates voice channels based on NFT data."""
        category = discord.utils.get(
            guild.categories, id=int(server_config['categoryID']))
        if not category:
            print(f"Category not found for server: {guild.id}")
            return

        existing_channels = {channel.name.split(":")[0].strip(
        ): channel for channel in category.voice_channels}
        configured_channels = server_config['board']['channels']

        await self.create_or_update_channels(guild, category, board_data, existing_channels, configured_channels)
        await self.cleanup_unused_channels(existing_channels, configured_channels)

    async def create_or_update_channels(self, guild, category, board_data, existing_channels, configured_channels):
        """Creates or updates channels based on the NFT data provided."""
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(connect=False)}
        for channel_name in configured_channels:
            new_channel_name = self.format_channel_name(
                channel_name, board_data)

            if statistic_channel_names[channel_name] in existing_channels:
                await existing_channels[statistic_channel_names[channel_name]].edit(name=new_channel_name)
            else:
                await guild.create_voice_channel(new_channel_name, category=category, overwrites=overwrites)

    async def cleanup_unused_channels(self, existing_channels, configured_channels):
        """Removes channels that are no longer needed."""
        for channel_name, channel in existing_channels.items():
            if channel_name not in statistic_channel_names_reverse or statistic_channel_names_reverse[channel_name] not in configured_channels:
                await channel.delete(reason="Cleaning up unused NFT data channels.")

    def format_channel_name(self, channel_name, board_data):
        """Formats the channel name based on the NFT data."""

        if channel_name in ['salesPast7d', 'salesPast24h', 'listed', 'totalOwners']:

            value = int(board_data[channel_name])

            return f"{statistic_channel_names[channel_name]}: {value}"
        else:
            value = float(board_data[channel_name]) / 10**9
            return f"{statistic_channel_names[channel_name]}: {value:.2f} SOL"

    @commands.command(name='setup')
    @commands.has_permissions(manage_channels=True)
    async def setup_nft_data(self, ctx):
        """Command to setup NFT data channels."""
        await self.update_server_nft_data(ctx.guild)
        await ctx.send("NFT data channels setup or updated.")

    @commands.command(name='cleanup')
    @commands.has_permissions(manage_channels=True)
    async def delete_channels(self, ctx):
        """Deletes all channels in the guild's NFT data category."""
        server_config = await self.get_server_config(ctx.guild.id)
        if not server_config:
            await ctx.send("This server does not have a collection configured.")
            return

        category = discord.utils.get(
            ctx.guild.categories, id=int(server_config['categoryID']))
        for channel in category.voice_channels:
            await channel.delete(reason="Cleaning up NFT data channels.")
        await ctx.send("All channels cleared.")


async def setup(bot):
    await bot.add_cog(Board(bot))
