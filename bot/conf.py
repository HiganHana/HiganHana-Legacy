from dataclasses import dataclass
from alib.bridge import Bridge
import logging

class BotConfig(Bridge):
    prefix = "~"
    case_insensitive = True
    cogs = []
    cog_folder = "bot_cogs"

    # flask
    host = "0.0.0.0"
    port = 8000
    blueprints_folder = "flask_cogs"

    # logging
    log_level = logging.DEBUG
    log_format = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"