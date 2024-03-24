from discord.ext import commands, tasks
import discord
from data.board_data import fetch_board_data
from data.admin_database import get_collection_discord_data, statistic_channel_names


class Board(commands.Cog):
    """Discord bot cog for managing NFT data boards."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Event listener for when the bot is ready."""
        if not self.update_nft_data.is_running():

            self.update_nft_data.start()

    @tasks.loop(minutes=5)
    async def update_nft_data(self):
        """Task loop to update NFT data."""
        for guild in self.bot.guilds:
            category = discord.utils.get(guild.categories, name=CATEGORY_NAME)
            if category:
                try:
                    board_data = await fetch_board_data()
                    existing_channel_names = {channel.name.split(
                        ":")[0].strip(): channel for channel in category.voice_channels}

                    for data_name, value in board_data.items():
                        formatted_value = float(value) / 10**9
                        new_channel_name = f"{data_name}: {formatted_value:.2f}SOL"

                        if data_name in existing_channel_names:
                            # Update existing channel
                            await existing_channel_names[data_name].edit(name=new_channel_name)
                        else:
                            # Create a new channel as it does not exist
                            overwrites = {
                                guild.default_role: discord.PermissionOverwrite(
                                    connect=False)
                            }
                            await guild.create_voice_channel(new_channel_name, category=category, overwrites=overwrites)

                    # Optionally, remove channels that no longer exist in the board_data
                    for channel_name, channel in existing_channel_names.items():
                        if channel_name not in board_data:
                            await channel.delete(reason="Cleaning up unused NFT data channels.")

                except Exception as e:
                    print(f"Error updating NFT data: {e}")

    @update_nft_data.before_loop
    async def before_update_nft_data(self):
        """Ensures the bot is ready before starting the task loop."""
        await self.bot.wait_until_ready()

    @commands.command(name='board')
    @commands.has_permissions(manage_channels=True)
    async def setup_nft_data(self, ctx):
        """Sets up voice channels for NFT data."""

        try:

            serverID = ctx.guild.id

            collection_server_config = get_collection_discord_data(serverID)

            collection_board_config = collection_server_config['board']

            if collection_server_config is None:
                await ctx.send("This server does not have a collection configured.")
                return

            categoryName = collection_board_config['category_name']
            channels = collection_board_config['channels']

            category = discord.utils.get(
                ctx.guild.categories, name=categoryName)
            if category:
                await ctx.send(f"The '{categoryName}' category already exists!")
                # No return here; proceed to update channels within this category
            else:
                # Create the category if it doesn't exist
                category = await ctx.guild.create_category(categoryName)
                await ctx.send(f"Created the '{categoryName}' category.")

            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(
                    connect=False)
            }

            stats = await fetch_board_data()

            for channel_name in channels:
                formatted_value = float(stats[channel_name]) / 10**9

                channel_full_name = f"{statistic_channel_names[channel_name]}: {formatted_value:.2f}SOL"

                existing_channel = discord.utils.get(
                    category.channels, name=channel_full_name)
                if not existing_channel:
                    await ctx.guild.create_voice_channel(channel_full_name, category=category, overwrites=overwrites)

        except Exception as e:
            await ctx.send(f"Failed to setup NFT data channels: {e}")

    @commands.command(name='dl')
    @commands.has_permissions(manage_channels=True)
    async def delete_channels(self, ctx):
        """Deletes all channels in the guild except for 'control'."""
        if ctx.guild is None:
            await ctx.send("This command can only be used in a server.")
            return

        for channel in ctx.guild.channels:
            if channel.name == "control":
                await ctx.send(f"Skipping {channel.name}")
                continue

            try:
                await channel.delete()
            except discord.Forbidden:
                await ctx.send(f"I do not have permission to delete {channel.name}.")
            except discord.HTTPException as e:
                await ctx.send(f"Failed to delete {channel.name}: {e}")

        await ctx.send("All channels and categories have been deleted.")


async def setup(bot):
    await bot.add_cog(Board(bot))
