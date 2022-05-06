
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
import bot.funcs as funcs

# ANCHOR
def run_bot_and_flask():
    # setup bot
    intents : discord.Intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    bot = commands.Bot(
        command_prefix=bot_bridge.prefix, 
        intents=intents,
        case_insensitive=bot_bridge.case_insensitive
    )
    bot_bridge._bot = bot

    #main cogs
    for cog in funcs.load_python_file(bot_bridge.cog_folder):
        logging.info(f"[bot init] Loading cog {bot_bridge.cog_folder}.{cog}")
        try:
            bot.load_extension(bot_bridge.cog_folder+"."+cog)
        except Exception as e:
            # stacktrace
            import traceback
            traceback.print_exc()
            logging.error(e)
            logging.error(f"[bot init] Failed to load cog {bot_bridge.cog_folder}.{cog}")

    #testing cogs
    for cog in funcs.load_python_file(bot_bridge.cog_building):
        logging.info(f"[bot init] Loading cog {bot_bridge.cog_building}.{cog}")
        try:
            bot.load_extension(bot_bridge.cog_building+"."+cog)
        except Exception as e:
            # stacktrace
            import traceback
            traceback.print_exc()
            logging.error(e)
            logging.error(f"[bot init] Failed to load cog {bot_bridge.cog_folder}.{cog}")

    # setup flask
    flask_app = Flask(__name__)
    # load blueprints dynamically
    for blueprint_name in funcs.load_python_file(bot_bridge.blueprints_folder):
        # add the blueprint to the list
        logging.info(f"[flask init] Loading blueprint {blueprint_name}")
        module = importlib.import_module(bot_bridge.blueprints_folder+"."+blueprint_name)
        flask_app.register_blueprint(getattr(module, blueprint_name))

    fthread = Thread(name="flask",target=flask_app.run, kwargs={"host": bot_bridge.host, "port": bot_bridge.port})
    fthread.start()
    logging.debug(f"[flask init] Flask thread started")
    logging.debug(f"[bot init] bot token: {bot_bridge.token}")

    @flask_app.route("/")
    def index():
        return "<h1>Bot is running</h1>"
    
    #
    if bot_bridge.no_bot:
        fthread.join()
    else:
        bot.run(bot_bridge.token)
