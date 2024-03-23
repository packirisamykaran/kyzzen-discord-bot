

from discord.ext import commands, tasks
from discord.utils import get
import discord
from data.board_data import fetch_nft_data
from config import CATEGORY_NAME


class Board(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def async_init(self):
        nft_data = await fetch_nft_data()
        self.total_listed = nft_data['total_listed']
        self.holders = nft_data['holders']

        print(f"Initialized total_listed: {self.total_listed}")

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.update_nft_data.is_running():
            await self.async_init()  # Asynchronously initialize the needed data
            self.update_nft_data.start()  # Then start your task loop

    @tasks.loop(minutes=10)
    async def update_nft_data(self):
        for guild in self.bot.guilds:
            category = discord.utils.get(
                guild.categories, name="Kyzzen NFT Data")
            if category:
                nft_data = await fetch_nft_data()

                # Assuming 'Total Listed' and 'Holders' channels exist
                # Update channel names with the latest data
                # Fetch the new data
                new_total_listed = nft_data['total_listed']
                new_holders = nft_data['holders']

                # Find channels by their previous names
                total_listed_channel = discord.utils.get(
                    category.voice_channels, name=f"total-listed-{self.total_listed}")
                holders_channel = discord.utils.get(
                    category.voice_channels, name=f"holders-{self.holders}")

                print(f"new listed: {new_total_listed}")

                # Update channels if they exist
                if total_listed_channel:

                    await total_listed_channel.edit(name=f"total-listed-{new_total_listed}")
                    self.total_listed = new_total_listed

                if holders_channel:
                    await holders_channel.edit(name=f"holders-{new_holders}")
                    self.holders = new_holders

                # print(
                #     f"Updating total-listed-{self.total_listed} to total-listed-{new_total_listed}")

    @update_nft_data.before_loop
    async def before_update_nft_data(self):
        await self.bot.wait_until_ready()

    @commands.command(name='board')
    @commands.has_permissions(manage_channels=True)
    async def setup_nft_data(self, ctx):
        guild = ctx.guild

        existing_category = discord.utils.get(
            guild.categories, name="Kyzzen NFT Data")
        if existing_category:
            await ctx.send("The 'Kyzzen NFT Data' category already exists!")
            return

        category = await guild.create_category("Kyzzen NFT Data")

        # Define read-only permissions for @everyone
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                connect=False,
            )
        }

        # Create channels with these overwrites
        await guild.create_voice_channel(f"total-listed-{self.total_listed}", category=category, overwrites=overwrites)
        await guild.create_voice_channel(f"holders-{self.holders}", category=category, overwrites=overwrites)

    @commands.command(name='dl')
    @commands.has_permissions(manage_channels=True)
    async def delete_channels(self, ctx):
        # Ensure the command is not executed in DMs
        if ctx.guild is None:
            await ctx.send("This command can only be used in a server.")
            return

        # Get a list of all text, voice channels, and categories
        channels = ctx.guild.channels  # This includes both channels and categories

        for channel in channels:
            if channel.name == "control":
                await ctx.send(f"Skipping {channel.name}")
                continue
            try:
                await channel.delete()
                # Optional: Send a confirmation message for each deletion
                # print(f"Deleted {channel.name}")
            except discord.Forbidden:
                await ctx.send(f"I do not have permission to delete {channel.name}.")
            except discord.HTTPException as e:
                await ctx.send(f"Failed to delete {channel.name}: {e}")

        await ctx.send("All channels and categories have been deleted.")


async def setup(bot):
    await bot.add_cog(Board(bot))
