from abc import abstractmethod
from dataclasses import dataclass
import logging
import os
import json 
import typing


class OnChangeDict(dict):
    """
    dict with changed flag
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hash = self._hash()

    def _hash(self):
        return hash(json.dumps(self, sort_keys=True))

    @property
    def changed(self):
        return self.hash != self._hash()

    def clear_changed(self):
        self.hash = self._hash()
        
@dataclass
class UID_Item:
    """
    vars without prefix _ will be directly saved to the referenced ArmandaTracker
    """

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
        self.__tracker__.__real_data__.pop(self.uid, None)

    def generate_keywords_var(self):
        for k in self.__keywords__:
            yield k,getattr(self, k)

    def update(self, **kargs):
        for k,v in kargs.items():
            if isinstance(v, tuple) and len(v) == 2 and callable(v[0]):

                if(v[0](v[1])):
                    setattr(self, k, v[1])
                continue
            
            setattr(self, k, v)


    def to_dict(self):
        return {k:v for k,v in self.generate_keywords_var()}
    


@dataclass
class HonkaiMember(UID_Item):
    discord_id : int
    lv : int
    __keywords__ = ["discord_id", "lv"]

class ArmandaTracker:

    def is_changed(self) -> bool:
        return self.__real_data__.changed

    def clear_changed(self) -> None:
        self.__real_data__.clear_changed()

    def __init__(
        self, 
        source : typing.Union[str, dict],
        typ : type, 
        halt_if_not_exist : bool = False,
        **kwargs
    ) -> None:
        self.__backup_path__ = None
        self.__real_data__ = OnChangeDict()

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
        
        
        for uid, item in rawdata.items():
            # item strip uid
            item : dict
            self.obj[uid] = typ(uid=int(uid),__tracker__=self, **item)

        self.clear_changed()

    def save(self, path : str =None) -> None:
        logging.info(f"{self} entered saving sequence")
        if self.__backup_path__ is None and path is None:
            raise ValueError("no path is given")
        if path is None:
            path = self.__backup_path__

        # if no change
        if not self.is_changed():
            logging.info(f"{self} no change, skip saving")
            return

        with open(path, "w") as f:
            logging.info(f"{self} saving to {path}")
            json.dump(self.__real_data__, f)

        self.clear_changed()

    def _get_dict(self, uid : int) -> dict:
        uid = str(uid)

        if uid not in self.__real_data__:
            return None
        return  self.__real_data__[uid]

    def _set_dict(self, uid : int, **kwargs) -> None:
        uid = str(uid)

        if uid not in self.__real_data__:
            self.__real_data__[uid] = OnChangeDict()
        self.__real_data__[uid].update(kwargs)

    def get_member(self, uid : int = None, **kwargs) -> UID_Item:
        uid = str(uid)
        if uid is not None and uid in self.obj:
            return self.obj[uid]

        if len(kwargs) == 0:
            return None

        for item in self.obj.values():
            if all(getattr(item, k) == v for k, v in kwargs.items()):
                return item

    def get_members(self, **kwargs) -> typing.List[UID_Item]:
        return [item for item in self.obj.values() if all(getattr(item, k) == v for k, v in kwargs.items())]

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
                else:
                    return True
        return False

    def remove_member(self, uid : int) -> UID_Item:
        if uid not in self.obj: 
            return False

        item = self.obj.pop(uid)
        del item

    def get_field(self,field : str,  uid : int = None, rtype=dict) -> typing.Any:
        """
        if uid provided, return the field of member
        if uid not provided, return the field of all members
        if field not found, return None
        """

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
        """
        same as get_field, but return generator
        """

        for item in self.obj.values():
            item : UID_Item
            target =getattr(item, field, None)
            if target is None:
                continue
            yield target