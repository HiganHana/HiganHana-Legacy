from discord.ext import commands
from discord.ext.commands import Bot
from bot.conf import bot_bridge
import discord
from discord.interactions import InteractionResponse
from bot_ui.reg import uid_form

class tester(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.slash_command(name="register", guild_ids=bot_bridge.allowed_servers)
    async def register(self, ctx):
        ires : InteractionResponse = ctx.interaction.response

        if ctx.author.id in bot_bridge._honkai_tracker.get_field_generator("discord_id"):
            embed = discord.Embed(title="Error", description="You are already registered")
            
            return await ires.send_message(embed=embed)

        form = uid_form()

        await ires.send_modal(form)
        bot_bridge._honkai_tracker.save()
    
    @commands.slash_command(name="unbind", guild_ids=bot_bridge.allowed_servers)
    @commands.has_any_role("Impact Vice Leader", "Impact Leader")
    async def unbind(self, ctx, user : discord.User):
        bot_bridge._honkai_tracker.remove_member_by_attr("discord_id", user.id)
        embed = discord.Embed(title="User Unbinded", description="Unbinded {}".format(user.mention))
        ires : InteractionResponse = ctx.interaction.response
        await ires.send_message(embed=embed)
        bot_bridge._honkai_tracker.save()

def setup(bot):
    bot.add_cog(tester(bot))