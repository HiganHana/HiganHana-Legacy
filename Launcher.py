from inspect import BoundArguments
from logging import NullHandler
from operator import le
from colorlog import LevelFormatter
import lightbulb
import hikari

bot = lightbulb.BotApp(token='ODkwNTIxMzM3MjAwNzc5MjY0.YUxAnw.tQjCovaWNKEttaRktcmzP-SMst0', #leaking this fine lmao, it's on a private server
    default_enabled_guilds=(773361373794402324)
)

#Event - Bot is running
@bot.listen(hikari.StartedEvent)
async def bot_started(event):
    print('Bot is running')

#Basic commands, will be move to Cogs later
@bot.command
@lightbulb.command('yahallo', 'new member use this')
@lightbulb.implements(lightbulb.SlashCommand)
async def yahallo(ctx):
    await ctx.respond('Welcome to the armada') #turn into embed and ping over at chill-chat


#Alert commands, move to Cogs later
@bot.command
@lightbulb.command('alert', 'turn on alert just for the user')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def alert_group(ctx):
    pass

@alert_group.child
@lightbulb.command('honkai', 'Honkai alert choices')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def subcommand(ctx):
    await ctx.respond('Honkai alert for you is on')

@alert_group.child
@lightbulb.command('hebban', 'Hebban alert choices')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def subcommand(ctx):
    await ctx.respond('Hebban alert for you is on')

#calculation commands (Cogs this shit)
@bot.command
@lightbulb.option('stat', 'Your Valk\'s current Crit Rate stat', type=int, required=True)
@lightbulb.option('level', 'Your Valk\'s current level', type=int, required=True)
@lightbulb.option('bonus', 'Only if it\'s necessary', type=int, required=False)
@lightbulb.command('valkcrit', 'Calculate your Valk\'s Crit Rate')
@lightbulb.implements(lightbulb.SlashCommand)
async def add(ctx):
    stat = ctx.options.stat
    level = ctx.options.level
    bonus = ctx.options.bonus
    if (bool(not bonus)):
        bonus = 0

    ret = ((stat / (level * 5 + 75)) * 100) + bonus
    await ctx.respond(f'Your valk\'s Crit Rate is: {ret}')

bot.run()