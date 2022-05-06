from turtle import title
import discord
from discord.ext import commands
from discord.bot import Bot
from bot.conf import bot_bridge

class help_command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
    #create a help command to guide people  
    help = discord.SlashCommandGroup("help", "Help you get familiar with this server")
      
    #Overall
    @help.command
    async def overall(ctx):
        embed = discord.embed(
            title = "Help - Hanabusa Cafe",
            description = "As long as you\'r following the #rules, you're free to do whatever"
        )
        embed.add_field(
            name = "Go get your roles",
            value = "If you haven\'t done that, then please do that so you unlock more chats",
            )
        embed.add_field(
            name = "Create a ticket",
            value = "If you wanna complains or something, create a ticket at #ticket-countertop, most information will be in there",
            )
        embed.add_field(
            name = "Annoucements/Events",
            value = "I rarely do annoucement unless it\'t related to server change or cyber-security stuff",
            )
        embed.add_field(
            name = "Limited time stuff",
            value = "Sometime there will be a limited time stuff that we do in this server, so be sure to look out for that",
            )
        embed.add_field(
            name = "Youtube/Twitch",
            value = "You make video or stream? Then you can post your content in the **Content Creator** catergory",
            )
        embed.add_field(
            name = "Content Creator",
            value = "Hand-picked content creator will get to post in #cc-uploaded-video and/or #cc-going-live, otherwise bot will do the posting",
            inline = True
            )
        embed.add_field(
            name = "Small Creator",
            value = "#youtube-video and #twitch-strem will be available for anyone to post",
            inline = True
            )
        await ctx.respond(embed = embed)
    
    #Hanabusa Cafe
    @help.command
    async def hanabusachat(ctx):
        embed = discord.embed(
            title = "Help - Hanabusa Cafe",
            value = "Please attempt to keep the topic in there, if you're talking about one unrelated stuff please move to another channel"
        )
        embed.add_field(
            name = "#chill-chat",
            value = "Basically talks about whatever, as long as it\'s SFW",
            inline = True
            )
        embed.add_field(
            name = "#bot-spam",
            value = "Use bot\'s commands here",
            inline = True
            )
        embed.add_field(
            name = "#horni-jail",
            value = "Very NSFW, join if you\'re willing to",
            inline = True
            )
        embed.add_field(
            name = "#shitpost-cave",
            value = "Post your shitpost, memes or laughable stuff here",
            inline = True
            )
        embed.add_field(
            name = "#art-channel",
            value = "Fan arts, drawing, etc. goes here, can be a slight ecchi but no hentai, that\'s for #horni-jail",
            inline = True
            )
        embed.set_footer(text = "If there\'s many request for a channel, I\' make one")
        await ctx.respond(embed = embed)
        
    #Honkai
    async def honkaiimpact(ctx):
        embed = discord.embed(
            title = "Help - Honkai Impact",
            value = "Don\'t hesitate to ask any questions and ping the helpers"
        )
        embed.add_field(
            title = "#impact-chat",
            value = "Honkai Impact related goes here, any questions will most likely be answered here",
            inline = True
            )
        embed.add_field(
            title = "#impact-annoucement",
            value = "Most of the annoucement related to Honkai or the armada will go here",
            inline = True
            )
        embed.add_field(
            title = "#impact-code",
            value = "If this chat glow white, there's a new code",
            inline = True
            )
        embed.add_field(
            title = "#impact-faq",
            value = "Honkai players\' bestfriend, be sure to check this first before asking any question",
            inline = True
            )
        embed.add_field(
            title = "#impact-lore",
            value = "All lore stuff will be discuss here to avoid spoilers in other chats",
            inline = True
            )
        embed.add_field(
            title = "#impact-leak-discussion",
            value = "Leaks, lots of leaks here",
            inline = True
            )
        embed.add_field(
            title = "#impact-coop",
            value = "Ask for a coop partner here",
            inline = True
            )
        embed.add_field(
            title = "#looking-for-sensei",
            value = "If you need a sensei or cadet, tell us here",
            inline = True
            )
        await ctx.respond(embed = embed)

def setup(bot):
    bot.add_cog(help_command(bot))

