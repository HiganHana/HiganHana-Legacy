import re
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from bot.conf import bot_bridge
import random

#Add daily reset I guess
#Add global pity cuz Cel is an evil bastard and I love it

class gacha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
gacha = discord.SlashCommandGroup("Gacha", "You fuking addict LMAO")

#single pull
@gacha.command()
async def single(self, ctx):
    result = the_math()
    embed = discord.Embed(
        title = "Here's your result you addict",
        value = f"{result}"
    )
    await ctx.respond(embed = embed)

#multi pulls
@gacha.command()
async def multi(self, ctx):
    
    result = []
    
    for x in range(10):
        result.append(the_math)
        
    embed = discord.Embed(
        title = "Here's your result you addict",
        value = result
    )
    await ctx.respond(embed = embed)
    
#Imma rig the living the shit out of this
# (based on Azur Lane cuz im too lazy to do the full math)
#3 type - SS (1%), S (10%), A(20%), Junk (69%)
def the_math(): 
    result = random.randint(1, 100)
    
    if result == 1:
        return str("SS")
    elif result > 1 and result <= 10:
        return str("S")
    elif result > 10 and result <= 20:
        return str("A")
    else:
        return str("Junk")

def setup(bot):
    bot.add_cog(gacha(bot))