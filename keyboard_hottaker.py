from typing import Any
import keyboard

class keyboard_hottaker:
    __is_take: bool
    __hotkey_callback: Any

    hotkey: str

    def is_take(self):
        return self.__is_take

    def __init__(self, hotkey: str):
        self.__is_take = False
        self.hotkey = hotkey
        self.__hotkey_callback = None

    def __take(self):
        self.__is_take = True
        keyboard.remove_hotkey(self.__hotkey_callback)
        self.__hotkey_callback = None

    def start(self):
        self.__is_take = False
        self.__hotkey_callback = keyboard.add_hotkey(self.hotkey, self.__take)

    def reset(self):
        self.__is_take = False
        if self.__hotkey_callback is not None:
            keyboard.remove_hotkey(self.__hotkey_callback)