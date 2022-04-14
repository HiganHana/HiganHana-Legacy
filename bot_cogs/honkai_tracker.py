from discord.ext import commands
from discord.ext.commands import Bot
from bot_ui.reg import ask_in_game_uid
from bot.conf import bot_bridge

class tester(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.slash_command(name="register", guild_ids=bot_bridge.allowed_servers)
    async def register(self, ctx):
        await ask_in_game_uid(ctx)
        bot_bridge._honkai_tracker.save()

def setup(bot):
    bot.add_cog(tester(bot))