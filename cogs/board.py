from discord.ext import commands, tasks
import discord
from data.board_data import fetch_board_data

# Constants
CATEGORY_NAME = "Kyzzen NFT Data"
TOTAL_LISTED_CHANNEL_PREFIX = "total-listed-"
HOLDERS_CHANNEL_PREFIX = "holders-"


listOfChannels = ["Holders", "Floor Price", ]


class Board(commands.Cog):
    """Discord bot cog for managing NFT data boards."""

    def __init__(self, bot):
        self.bot = bot
        self.total_listed = None
        self.holders = None

    async def async_init(self):
        """Asynchronously initializes cog data."""
        try:
            nft_data = await fetch_nft_data()
            self.total_listed = nft_data['total_listed']
            self.holders = nft_data['holders']
            print(f"Initialized total_listed: {self.total_listed}")
        except Exception as e:
            print(f"Error initializing Board cog: {e}")

    @commands.Cog.listener()
    async def on_ready(self):
        """Event listener for when the bot is ready."""
        if not self.update_nft_data.is_running():
            await self.async_init()
            self.update_nft_data.start()

    @tasks.loop(minutes=10)
    async def update_nft_data(self):
        """Task loop to update NFT data."""
        for guild in self.bot.guilds:
            category = discord.utils.get(guild.categories, name=CATEGORY_NAME)
            if category:
                try:
                    board_data = await fetch_board_data()

                    for channel in category.voice_channels:
                        channel_name = channel.name.split(":")[0].strip()
                        if channel_name in board_data:
                            formatted_value = float(
                                board_data[channel_name]) / 10**9
                            await channel.edit(name=f"{channel_name}: {formatted_value:.2f}")
                            print(
                                f"Updated {channel_name} to {formatted_value:.2f}")

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

        category = discord.utils.get(ctx.guild.categories, name=CATEGORY_NAME)
        if category:
            await ctx.send(f"The '{CATEGORY_NAME}' category already exists!")
            return

        try:
            category = await ctx.guild.create_category(CATEGORY_NAME)

            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(connect=False)}

            stats = await fetch_board_data()

            # Loop through the list of channels and create them
            for channel_name, value in stats.items():
                formatted_value = float(value) / 10**9
                await ctx.guild.create_voice_channel(f"{channel_name}: {formatted_value:.2f}", category=category, overwrites=overwrites)

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
