"""
this file contains the global configurations

BotBridge will load the specified json file with dict.update(), overwriting existing keys
"""

from dataclasses import dataclass
import typing
from alib.bridge import Bridge
import logging

from alib.tracker import ArmandaTracker, HonkaiMember

class BotBridge(Bridge):
    prefix = "!"
    case_insensitive = True
    cogs = []
    cog_folder = "bot_cogs"
    allowed_servers : typing.List[int]
    token : str
    no_bot : bool = False

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
    _honkai_tracker : ArmandaTracker = ArmandaTracker("appdata/honkai_members.json" , typ=HonkaiMember)

    # permissions
    MOD_ROLES = ["Impact Vice Leader", "Impact Leader","admin"]

bot_bridge : BotBridge = BotBridge(file="appdata/config.json")