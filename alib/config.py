import json
from alib.misc import is_jsonable

class Config:
    def __init__(self, file=None, skip_if_null : bool = True, save_non_serial : bool = True) -> None:

        self._ignoresave = True
        self._filename = None
        self._config = {}
        self._save_non_serial = save_non_serial

        if file is None and not skip_if_null:
            raise Exception("No config file specified")
        try:
            with open(file, "r") as f:
                raw_config = json.load(f)
                self._config.update(raw_config)

            self._filename = file
        except:
            if not skip_if_null:
                raise
        self._ignoresave = False

    def __getattr__(self, name: str):
        if name in self._config:
            return self._config[name]

        return super().__getattribute__(name)

    def __setattr__(self, name: str, val) -> None:
        if not name.startswith("_"):
            self._config[name] = val
            self._save()
        else:
            super().__setattr__(name, val)

    def _wrap_export_config(self):
        if self._save_non_serial:
            return self._config
        else:
            dump_dict = {}
            # ignore non jsonable values
            for key, val in self._config.items():
                if is_jsonable(val):
                    dump_dict[key] = val

            return dump_dict

    def _save(self) -> None:
        """
        Save the config to the file
        if _ignoresave is True, this will not save
        if 
        """

        if self._ignoresave:
            return
        if self._filename is None:
            return
        with open(self._filename, "w") as f:
            data = self._wrap_export_config()

            json.dump(data, f, indent=4)

    