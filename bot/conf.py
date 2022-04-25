"""
this file contains the global configurations

BotBridge will load the specified json file with dict.update(), overwriting existing keys
"""

from dataclasses import dataclass
import typing
from zxutil.collections.bridge import Bridge
import logging

from zxutil.collections.uitem import UTracker
from bot.tracker import ArmandaMember, verfication_model

import honkaiDex.profile.cached

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
    log_to_file = False
    log_file = "bot.log"

    #
    _honkai_tracker : UTracker = UTracker(
        uitem_type=ArmandaMember,
        data="appdata/honkai_members.json",
        verification_model=verfication_model
    )

    # permissions
    MOD_ROLES = ["Impact Vice Leader", "Impact Leader","admin"]

    # hoyo
    ltuid : int
    ltoken : str

bot_bridge : BotBridge = BotBridge(file="appdata/config.json")