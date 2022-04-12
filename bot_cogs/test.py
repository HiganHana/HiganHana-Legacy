from discord.ext import commands
from discord.ext.commands import Bot
from armandaTracker.q_account import ask_in_game_uid
from bot.conf import config

class tester(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.slash_command(name="hello", guild_ids=config.allowed_servers)
    async def hello(self, ctx):
        await ask_in_game_uid(ctx)


def setup(bot):
    bot.add_cog(tester(bot))