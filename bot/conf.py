from dataclasses import dataclass
from alib.bridge import Bridge
import logging

from alib.tracker import ArmandaTracker, HonkaiMember

class BotBridge(Bridge):
    prefix = "!"
    case_insensitive = True
    cogs = []
    cog_folder = "bot_cogs"
    allowed_servers = [773361373794402324]
    token : str

    # flask
    host = "0.0.0.0"
    port = 8000
    blueprints_folder = "flask_cogs"

    # logging
    log_level = logging.DEBUG
    log_format = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
    
    log_ignore_discord = True
    log_sysout = True
    log_file = "bot.log"

    #
    _honkai_tracker : ArmandaTracker = ArmandaTracker("appdata/honkai_members.json")

bot_bridge : BotBridge = BotBridge(file="appdata/config.json")