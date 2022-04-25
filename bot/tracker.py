from dataclasses import dataclass
from zxutil.collections.uitem import UItem, UTracker, UniqueConflict, UniqueKey, PrimaryJsonKey
from honkaiDex.game import valid_lv
@dataclass
class ArmandaMember(UItem):
    discord_id : PrimaryJsonKey
    uid : UniqueKey
    lv : int
    genshin_id : UniqueKey = None

verfication_model = {
    "lv": valid_lv,
    "uid" : int
}

