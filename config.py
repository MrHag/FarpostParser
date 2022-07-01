import json
from typing import Any, List


class config:

    __filename: str

    browser_type: str
    browser_path: str
    exit_hotkey: str
    pause_hotkey: str

    def __init__(self, filename):
        self.__filename = filename
        self.__load_or_def()

    def _default_config(self) -> dict[str, Any]:
        raise NotImplementedError()

    def _cast_and_write(self, conf: Any):
        raise NotImplementedError()

    def __create_default_config(self) -> dict[str, Any]:
        defconf = self._default_config()
        defconf.update({'browser_type': "chrome", 'browser_path': '', 'exit_hotkey': 'alt+f', 'pause_hotkey': 'alt+p'})
        with open(self.__filename, 'w') as configIO:
            json.dump(defconf, configIO)

        return defconf

    def __cast_and_write(self, conf: Any):
        try:
            self._cast_and_write(conf)
            self.browser_type = conf['browser_type'].lower()
            self.browser_path = conf['browser_path']
            self.exit_hotkey = conf['exit_hotkey']
            self.pause_hotkey = conf['pause_hotkey']
        except Exception:
            raise InvalidConfigException

    def __load_or_def(self):
        conf: dict[str, Any]

        try:
            with open(self.__filename, 'r') as f:
                conf = json.load(f)

            self.__cast_and_write(conf)
        except Exception:
            self.__create_default_config()
            raise InvalidConfigException
            


class InvalidConfigException(Exception):
    """Raised when the config is invalid"""
    pass
