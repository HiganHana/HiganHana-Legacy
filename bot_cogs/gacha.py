import discord
from discord.ext import commands
from discord.ext.commands import Bot
from bot.conf import bot_bridge

S_RANK = 1
A_RANK = 2

class gacha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
gacha = discord.SlashCommandGroup("Gacha", "You fuking addict LMAO")

#single pull
@gacha.command()
async def single(self, ctx):
    
    await ctx.respond()

#multi pulls
@gacha.command()
async def multi(self, ctx):
    
    await ctx.respond()

#Imma rig the living the shit out of this
def the_math() -> int:
    
    return