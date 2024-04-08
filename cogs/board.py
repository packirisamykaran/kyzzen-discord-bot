import discord
from discord.ext import commands, tasks
from data.board_data import fetch_board_data
from admin_database import get_collection_discord_data, statistic_channel_names, statistic_channel_names_reverse


class Board(commands.Cog):
    """Discord bot cog for managing NFT data boards."""

    def __init__(self, bot):
        self.bot = bot
        self.update_nft_data.start()  # Start the task when the cog is loaded

    def cog_unload(self):
        """Clean up resources when the cog is removed."""
        self.update_nft_data.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        """Event listener for when the bot is ready."""
        print("Board cog is ready and running.")

    @tasks.loop(minutes=10)
    async def update_nft_data(self):
        """Task loop to update NFT data across all servers."""
        print('updating NFT data for all servers')
        for guild in self.bot.guilds:
            await self.update_server_nft_data(guild)

    @update_nft_data.before_loop
    async def before_update_nft_data(self):
        """Wait for the bot to be ready before starting the loop."""
        await self.bot.wait_until_ready()

    async def update_server_nft_data(self, guild):
        """Fetches and updates NFT data voice channels for a guild."""
        server_config = await self.get_server_config(guild.id)
        if not server_config:
            return

        collection_id = server_config['collectionID']

        board_data = await fetch_board_data(collection_id)
        await self.manage_voice_channels(guild, server_config, board_data)

    async def get_server_config(self, guild_id):
        """Fetches server configuration for NFT board."""
        config = get_collection_discord_data(guild_id)
        if config and 'board' in config and 'categoryID' in config:
            return config
        print(f"Configuration incomplete or not found for server: {guild_id}")
        return None

    async def manage_voice_channels(self, guild, server_config, board_data):
        """Manages the creation and updating of voice channels for NFT data."""
        category_id = int(server_config['categoryID'])
        category = discord.utils.get(guild.categories, id=category_id)
        if not category:
            print(f"Category ID {category_id} not found in guild: {guild.id}")
            return

        existing_channels = {ch.name.split(
            ":")[0].strip(): ch for ch in category.voice_channels}
        configured_channels = server_config['board']['channels']

        await self.sync_channels(guild, category, board_data, existing_channels, configured_channels)

    async def sync_channels(self, guild, category, board_data, existing_channels, configured_channels):
        """Creates or updates channels and cleans up unused ones."""
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(connect=False)}
        for channel_name in configured_channels:
            formatted_name = self.format_channel_name(channel_name, board_data)
            original_name = statistic_channel_names[channel_name]
            if original_name in existing_channels:
                await existing_channels[original_name].edit(name=formatted_name)
            else:
                await guild.create_voice_channel(formatted_name, category=category, overwrites=overwrites)

        await self.cleanup_channels(existing_channels, configured_channels)

    async def cleanup_channels(self, existing_channels, configured_channels):
        """Deletes unused voice channels from the NFT data category."""
        for original_name, channel in existing_channels.items():
            if original_name not in statistic_channel_names_reverse or statistic_channel_names_reverse[original_name] not in configured_channels:
                await channel.delete(reason="NFT data channel cleanup")

    def format_channel_name(self, channel_name, board_data):
        """Formats the channel name with the relevant NFT data statistic."""
        value = board_data[channel_name]
        formatted_name = statistic_channel_names[channel_name]
        if channel_name in ['salesPast7d', 'salesPast24h', 'listed', 'totalOwners']:
            return f"{formatted_name}: {int(value)}"
        return f"{formatted_name}: {float(value) / 10**9:.2f} SOL"

    @commands.command(name='setup')
    @commands.has_permissions(manage_channels=True)
    async def setup_nft_data(self, ctx):
        """Command to setup or update NFT data channels in the server."""
        await self.update_server_nft_data(ctx.guild)
        await ctx.send("NFT data channels are set up or updated.")

    @commands.command(name='cleanup')
    @commands.has_permissions(manage_channels=True)
    async def delete_channels(self, ctx):
        """Command to delete all NFT data channels in the server."""
        server_config = await self.get_server_config(ctx.guild.id)
        if not server_config:
            await ctx.send("Server configuration not found.")
            return

        category = discord.utils.get(
            ctx.guild.categories, id=int(server_config['categoryID']))
        if category:
            for channel in category.voice_channels:
                await channel.delete(reason="NFT data channel cleanup by command")
            await ctx.send("NFT data channels have been cleared.")


async def setup(bot):
    """Function to add this cog to a bot."""
    await bot.add_cog(Board(bot))
