from typing import Any
import keyboard

from keyboard_hottaker import keyboard_hottaker

class exiter:
    __exit_state: keyboard_hottaker
    __pause_state: keyboard_hottaker

    def is_exit(self) -> bool:
        return self.__exit_state.is_take()

    def pause(self):
        if self.__pause_state.is_take():
            input("Program on pause...")
            self.__pause_state.start()

    def __init__(self, exit_hotkey: str, pause_hotkey: str):
        self.__exit_state = keyboard_hottaker(exit_hotkey)
        self.__pause_state = keyboard_hottaker(pause_hotkey)
        self.__exit_state.start()
        self.__pause_state.start()
        
    def reset(self):
        self.__exit_state.reset()
        self.__pause_state.reset()
        self.__exit_state.start()
        self.__pause_state.start()
