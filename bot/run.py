import os
from pprint import pprint
import discord
from discord.ext import commands
import logging
import sys
from flask import Flask
from threading import Thread
import importlib

# add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.conf import config



if __name__ == "__main__":

    # setup logging
    logging.basicConfig(level=config.log_level, format=config.log_format, filename="bot.log")
    #logging.getLogger("discord").setLevel(logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    # setup bot
    intents : discord.Intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    bot = commands.Bot(
        command_prefix=config.prefix, 
        intents=intents,
        #case_insensitive=True
    )


    cogs = []
    # get all py files in cogs folder
    for file in os.listdir(config.cog_folder):
        if file.endswith(".py"):
            # get the name of the file without the .py extension
            cog_name = file[:-3]
            # add the cog to the list
            cogs.append(cog_name)


    for cog in cogs:
        logging.info(f"[bot init] Loading cog {config.cog_folder}.{cog}")
        bot.load_extension(config.cog_folder+"."+cog)


    # setup flask
    flask_app = Flask(__name__)
    # load blueprints dynamically
    for file in os.listdir(config.blueprints_folder):
        if file.endswith(".py"):
            # get the name of the file without the .py extension
            blueprint_name = file[:-3]
            # add the blueprint to the list
            logging.info(f"[flask init] Loading blueprint {blueprint_name}")
            module = importlib.import_module(config.blueprints_folder+"."+blueprint_name)
            flask_app.register_blueprint(getattr(module, blueprint_name))

    fthread = Thread(name="flask",target=flask_app.run, kwargs={"host": config.host, "port": config.port})
    fthread.start()
    logging.debug(f"[flask init] Flask thread started")
    logging.debug(f"[bot init] bot token: {config.token}")
    bot.run(config.token)