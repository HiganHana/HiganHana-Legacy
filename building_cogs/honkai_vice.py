import discord
from discord.ext import commands
from discord.ext.commands import Bot
from bot.conf import bot_bridge

class honkai_vice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    #give or remove Impact-Member roles to the person
    armada = discord.SlashCommandGroup("armada", "manage armada member")
    
    @armada.command()
    async def add(self, ctx, user : discord.User = None):
        
        if user is None:
            embed = discord.Embed(title="Error", description= "Put a name down dumbass lmao")
            return await ctx.respond(embed=embed)
        
        else:
            embed = discord.Embed(title="Welcome to the armada!", description= f"Added {user.mention}, remember to do Sim Battle when it reset")
        await ctx.respond(embed = embed)
    
    
    @armada.command()
    async def remove(self, ctx, user : discord.User = None):
        
        if user is None:
            embed = discord.Embed(title="Error", description= "Put a name down dumbass lmao")
            return await ctx.respond(embed=embed)
        
        else:
            embed = discord.Embed(title="Awww you left us", description= f"{user.mention} you can always reapply")
        await ctx.respond(embed = embed)

def setup(bot):
    bot.add_cog(honkai_vice(bot))