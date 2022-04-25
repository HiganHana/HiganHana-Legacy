from datetime import datetime, tzinfo, time
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from bot.conf import bot_bridge
import random
from discord.ext import tasks

gachagroup : discord.SlashCommandGroup = discord.SlashCommandGroup("gacha", "Gacha commands")
# 8 am utc
RESET_TIME = time(8, 0, 0)

class gacha_cog(commands.Cog):
    def __init__(self, bot):
        self.GLOBAL_PITY_COUNT = 0
        self.GLOBAL_PITY_MAX =random.randint(50,100000) #Fucking 100,000 for pity, Cel is an evil bastard and I love it
        # get next day at utc 
        
        self.bot : discord.Bot = bot
        self.daily_reset.start()
        
    #single pull
    @gachagroup.command()
    async def single(self, ctx):
        result = self.the_math()
        
        if self.global_pity():
            result = "SS"
        
        embed = discord.Embed(
            title = "Here's your result you addict",
            value = f"{result}"
        )
        embed.add_field(title = "Server Pity Count", value = f"{self.GLOBAL_PITY_COUNT}/{self.GLOBAL_PITY_MAX}")
        
        await ctx.respond(embed = embed)

    #multi pulls
    @gachagroup.command()
    async def multi(self, ctx):
        
        result = []
        
        for x in range(10):
            result.append(self.the_math())
            
        if self.global_pity():
            result[9] = "SS"
            
        embed = discord.Embed(
            title = "Here's your result you addict",
            value = f"{result}"
        )
        embed.add_field(title = "Server Pity Count", value = f"{self.GLOBAL_PITY_COUNT}/{self.GLOBAL_PITY_MAX}")
        
        await ctx.respond(embed = embed)
        
    #Imma rig the living the shit out of this
    # (based on Azur Lane cuz im too lazy to do the full math)
    #3 type - SS (1%), S (10%), A(20%), Junk (69%)
    def the_math(self): 
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
    def global_pity(self, increase : int = 0):
        
        if self.GLOBAL_PITY_COUNT + increase >= self.GLOBAL_PITY_MAX:
            self.GLOBAL_PITY_MAX = random.int(50,100000)
            return True
        else:
            self.GLOBAL_PITY_COUNT += increase
            return False

    #daily reset
    @tasks.loop(time=RESET_TIME)
    async def daily_reset(self, ctx):

        self.GLOBAL_PITY_COUNT = 0
        self.GLOBAL_PITY_MAX = random.randint(50,100000)
        channel = self.bot.get_channel(766134112028983326)
        
        embed = discord.Embed(
            title = "Server Gacha Resetted",
            value = f"The new pity is {self.GLOBAL_PITY_MAX}, good luck yall!"
        )
        await channel.send(embed = embed)
    

def setup(bot : discord.Bot):
    bot.add_cog(gacha_cog(bot))