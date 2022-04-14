from abc import abstractmethod
import asyncio
from dataclasses import dataclass
import logging
import os
import json 
import typing


class OnChangeDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.changed = False

    def __setitem__(self, key, value):
        if key in self and self[key] == value:
            return
        super().__setitem__(key, value)
        self.changed = True
    
    def __delitem__(self, key):
        super().__delitem__(key)
        self.changed = True
    
    def clear(self):
        super().clear()
        self.changed = True

    def pop(self, key, default=None):
        super().pop(key, default)
        self.changed = True
    
    def popitem(self):
        super().popitem()
        self.changed = True
    
    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self.changed = True

    def set_changed(self, changed):
        self.changed = changed

    def clear_changed(self):
        self.changed = False

    def is_changed(self):
        return self.changed

@dataclass
class UID_Item:
    __tracker__ : 'ArmandaTracker'
    __keywords__ = []
    uid : int

    def __setattr__(self,name : str, val) -> None:
        if not name.startswith("_") and name in self.__keywords__:
            return self.__tracker__._set_dict(self.uid, **{name:val})
        return super().__setattr__(name, val)
        

    def __getattr__(self,name : str) -> None:
        if not name.startswith("_") and name in self.__keywords__:
            return self.__tracker__._get_dict(self.uid)[name]
        return super().__getattr__(name)

    def __delattr__(self,name : str) -> None:
        if not name.startswith("_") and name in self.__keywords__:
            self.__tracker__.__real_data__.pop(name)
            return
        return super().__delattr__(name)

    def __del__(self) -> None:
        self.__tracker__.__real_data__.pop(self.uid)

@dataclass
class HonkaiMember(UID_Item):
    discord_id : int
    lv : int
    __keywords__ = ["discord_id", "lv"]

class ArmandaTracker:


    def __init__(
        self, 
        source : typing.Union[str, dict],
        typ : type, 
        halt_if_not_exist : bool = False,
        **kwargs
    ) -> None:
        self.__backup_path__ = None

        if isinstance(source, str) and not os.path.exists(source):
            if halt_if_not_exist:
                raise FileNotFoundError(source)
            folder = os.path.dirname(source)
            if folder is not None and folder != "":
                os.makedirs(folder, exist_ok=True)
            with open(source, "w") as f:
                json.dump({}, f)

        if isinstance(source, str):
            self.__backup_path__ = source 

            with open(source, "r") as f:
                rawdata = json.load(f)
        elif isinstance(source, dict):
            rawdata = source
        else:
            raise TypeError(f"source must be str or dict, but got {type(source)}")


        self.ctype = typ
        
        self.obj = {}
        self.__real_data__ = OnChangeDict()
        
        for uid, item in rawdata.items():
            # item strip uid
            item : dict
            self.obj[uid] = typ(uid=int(uid),__tracker__=self, **item)

        

    def save(self, path : str =None) -> None:
        logging.info(f"{self} entered saving sequence")
        if self.__backup_path__ is None and path is None:
            raise ValueError("no path is given")
        if path is None:
            path = self.__backup_path__

        with open(path, "w") as f:
            json.dump(self.__real_data__, f)

    def _get_dict(self, uid : int) -> dict:
        uid = str(uid)

        if uid not in self.__real_data__:
            return None
        return  self.__real_data__[uid]

    def _set_dict(self, uid : int, **kwargs) -> None:
        uid = str(uid)

        if uid not in self.__real_data__:
            self.__real_data__[uid] = {}
        
        self.__real_data__[uid].update(kwargs)

    def get_member(self, uid : int) -> UID_Item:
        return self.obj.get(str(uid), None)

    def has_member(self, uid : int) -> bool:
        return uid in self.obj

    def add_member(self, uid : int, **kwargs) -> UID_Item:
        if uid in self.obj:
            return None
    
        item = self.ctype(uid=uid, __tracker__=self, **kwargs)
        self.obj[uid] = item
        return item

    def remove_member_by_attr(self, attr : str, value : typing.Any, more_than_1 : bool = False) -> None:
        for uid, item in self.obj.items():
            if getattr(item, attr) == value:
                self.obj.pop(uid)
                if more_than_1:
                    continue
                break

    def remove_member(self, uid : int) -> UID_Item:
        if uid not in self.obj: 
            return False

        item = self.obj.pop(uid)
        del item

    def get_field(self,field : str,  uid : int = None, rtype=dict) -> typing.Any:
        if uid is not None and uid not in self.obj:
            return None
        if uid is not None:
            return getattr(self.obj[uid], field)

        if rtype != dict and rtype != list:
            raise TypeError(f"rtype must be dict or list, but got {rtype}")
        
        if rtype == dict:
            ret = {}
            for item in self.obj.values():
                item : UID_Item
                target =getattr(item, field, None)
                if target is None:
                    continue
                ret[str(item.uid)] = target

        if rtype == list:
            ret = []
            for item in self.obj.values():
                item : UID_Item
                target =getattr(item, field, None)
                if target is None:
                    continue
                ret.append(target)

        return ret

    def get_field_generator(self, field: str):
        for item in self.obj.values():
            item : UID_Item
            target =getattr(item, field, None)
            if target is None:
                continue
            yield target