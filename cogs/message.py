from discord.ext import commands


class MessageCommands(commands.Cog):
    """
    A cog for simple message-based commands.
    This cog includes commands for greeting and farewells.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hi')
    async def hi(self, ctx):
        """
        Responds with a greeting message.
        """
        await ctx.send('Hello!')

    @commands.command(name='bye')
    async def bye(self, ctx):
        """
        Responds with a farewell message.
        """
        await ctx.send('Goodbye!')

    # Consider adding error handling within your commands to manage common issues,
    # such as permissions errors, or to provide custom feedback for command-specific errors.


async def setup(bot):
    """
    The setup function to add this cog to a bot.
    """
    await bot.add_cog(MessageCommands(bot))
