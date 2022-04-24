from datetime import datetime, tzinfo
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from bot.conf import bot_bridge
import random
from discord.ext import tasks

GLOBAL_PITY_COUNT = 0
GLOBAL_PITY_MAX = random.int(50,100000) #Fucking 100,000 for pity, Cel is an evil bastard and I love it
DAILY_RESET = datetime.time(hour=9, tzinfo="UTC") #9am UTC cuz fuck daylight saving

class gacha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        daily_reset.start()
        
gacha = discord.SlashCommandGroup("Gacha", "You fuking addict LMAO")

#single pull
@gacha.command()
async def single(self, ctx):
    result = the_math()
    
    if global_pity:
        result = "SS"
    
    embed = discord.Embed(
        title = "Here's your result you addict",
        value = f"{result}"
    )
    embed.add_field(title = "Server Pity Count", value = f"{GLOBAL_PITY_COUNT}/{GLOBAL_PITY_MAX}")
    
    await ctx.respond(embed = embed)

#multi pulls
@gacha.command()
async def multi(self, ctx):
    
    result = []
    
    for x in range(10):
        result.append(the_math)
        
    if global_pity:
        result[9] = "SS"
        
    embed = discord.Embed(
        title = "Here's your result you addict",
        value = f"{result}"
    )
    embed.add_field(title = "Server Pity Count", value = f"{GLOBAL_PITY_COUNT}/{GLOBAL_PITY_MAX}")
    
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

#time to make everyone piss
def global_pity(increase : int = 0):
    
    if GLOBAL_PITY_COUNT + increase >= GLOBAL_PITY_MAX:
        GLOBAL_PITY_MAX = random.int(50,100000)
        return True
    else:
        GLOBAL_PITY_COUNT =+ increase
        return False

#daily reset
@tasks.loop(time=DAILY_RESET)
async def daily_reset(self, ctx):
    GLOBAL_PITY_COUNT = 0
    GLOBAL_PITY_MAX = random.int(50,100000)
    channel = self.bot.get_channel(766134112028983326)
    
    embed = discord.Embed(
        title = "Server Gacha Resetted",
        value = f"The new pity is {GLOBAL_PITY_MAX}, good luck yall!"
    )
    await channel.send(embed = embed)
    

def setup(bot):
    bot.add_cog(gacha(bot))