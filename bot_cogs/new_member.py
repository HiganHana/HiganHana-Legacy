from turtle import title
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from bot_ui.reg import ask_in_game_uid
from bot.conf import bot_bridge

class new_member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    #Fresh people join this discord TODO add embed and infomation,
    @commands.slash_command(name="yahallo", guild_ids=bot_bridge.allowed_servers)
    async def new_member(self, ctx, member: discord.Member):
        #Create embed
        embed = discord.Embed(
            title = "Welcome to HiganHana",
            description = "Welcome to the server @{member.name}! Check out #chill-chat to give yourself a role!",
            color = discord.colour.red(),
        )
        
        #Honkai Impact field
        embed.add_field(
            title = "Honkai Impact Players",
            value = "If you're applying or already in the armada, **Please use the command /register to get started**"
        )
        
        #Honkai Star Rail
        embed.add_field(
            title = "Honkai Star Rail Players",
            value = "The game is currently in a closed contracted beta test, please avoid leaking anything here cuz last thing I need is a lawsuit on my ass"
        )
        
        #Hebban field
        embed.add_field(
            title = "Heaven Burns Red Players",
            value = "Kiyan can answer some questions so don't hesitate to ask him"
        )
        await ctx.respond(embed = embed)
    
 

def setup(bot):
    bot.add_cog(new_member(bot))