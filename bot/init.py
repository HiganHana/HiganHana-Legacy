
import os
from pprint import pprint
import discord
from discord.ext import commands
import logging
import sys
from flask import Flask
from threading import Thread
import importlib
from bot.conf import bot_bridge


# ANCHOR
def run_bot_and_flask():
    # setup logging
    logging.basicConfig(level=bot_bridge.log_level, format=bot_bridge.log_format, stream=sys.stdout)

    if not bot_bridge.log_ignore_discord:
        logging.getLogger("discord").setLevel(logging.DEBUG)
    if bot_bridge.log_to_file:
        logging.getLogger().addHandler(logging.FileHandler(bot_bridge.log_file))

    # setup bot
    intents : discord.Intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    bot = commands.Bot(
        command_prefix=bot_bridge.prefix, 
        intents=intents,
        case_insensitive=bot_bridge.case_insensitive
    )


    cogs = []
    # get all py files in cogs folder
    for file in os.listdir(bot_bridge.cog_folder):
        if file.endswith(".py"):
            # get the name of the file without the .py extension
            cog_name = file[:-3]
            # add the cog to the list
            cogs.append(cog_name)


    for cog in cogs:
        logging.info(f"[bot init] Loading cog {bot_bridge.cog_folder}.{cog}")
        try:
            bot.load_extension(bot_bridge.cog_folder+"."+cog)
        except Exception as e:
            # stacktrace
            import traceback
            traceback.print_exc()
            logging.error(e)
            logging.error(f"[bot init] Failed to load cog {bot_bridge.cog_folder}.{cog}")


    # setup flask
    flask_app = Flask(__name__)
    # load blueprints dynamically
    for file in os.listdir(bot_bridge.blueprints_folder):
        if file.endswith(".py"):
            # get the name of the file without the .py extension
            blueprint_name = file[:-3]
            # add the blueprint to the list
            logging.info(f"[flask init] Loading blueprint {blueprint_name}")
            module = importlib.import_module(bot_bridge.blueprints_folder+"."+blueprint_name)
            flask_app.register_blueprint(getattr(module, blueprint_name))

    fthread = Thread(name="flask",target=flask_app.run, kwargs={"host": bot_bridge.host, "port": bot_bridge.port})
    fthread.start()
    logging.debug(f"[flask init] Flask thread started")
    logging.debug(f"[bot init] bot token: {bot_bridge.token}")

    #
    if bot_bridge.no_bot:
        fthread.join()
    else:
        bot.run(bot_bridge.token)
