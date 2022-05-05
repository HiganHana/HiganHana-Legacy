from turtle import title
import discord
from discord.ext import commands
from discord.bot import Bot
from bot.conf import bot_bridge

class new_member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
       
        
    #Fresh people join this discord TODO add embed and infomation,
    @commands.slash_command(
        name="yahallo",
        guild_ids=bot_bridge.allowed_servers,
        description="Give tags to newly joined member"
        )
    async def new_member(self, ctx):
        #Create embed
        embed = discord.Embed(
            title = "Welcome to HiganHana",
            description = f"Welcome to the server @{ctx.author.name}! Check out #chill-chat to give yourself a role!",
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

        await ctx.respond(embed = embed)


def setup(bot):
    bot.add_cog(new_member(bot))

