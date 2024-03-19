from discord.ext import commands


class MessageCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('MessageCommands initialized')

    @commands.command(name='hi')
    async def hi(self, ctx):
        await ctx.send('Hello!')


async def setup(bot):
    await bot.add_cog(MessageCommands(bot))
