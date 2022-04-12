from discord.ext import commands
from discord.ext.commands import Bot


class tester(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def test(self, ctx):
        await ctx.send("test")


def setup(bot):
    bot.add_cog(tester(bot))