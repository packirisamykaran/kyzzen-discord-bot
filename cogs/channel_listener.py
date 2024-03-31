
# This cog listens to messages in a channel and stores them in a database.

from data.channel_data import store_message
from discord.ext import commands


class ChannelListener(commands.Cog):
    """
    A cog for listening to messages in a channel.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Listen to channelID and store messages in a database.
        """

        print(f"Message from {message.author}: {message.content}")

        # Check if the message is from the correct channel
        if message.channel.id == 1222544109261291712:
            print(f"Message from {message.author}: {message.content}")
            store_message({"content": message.content})


async def setup(bot):
    await bot.add_cog(ChannelListener(bot))
