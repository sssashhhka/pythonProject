import os
import time

version: str = "Log v.2.0 stable"


class Log:
    def __init__(self, silent_mode: bool = False):
        self.state: str = "None"
        self.sys_info: str = "None"
        self.info: str = "None"
        self.file = None
        self.is_silent_mode = silent_mode

    def console_out(self, info: str, state: str):
        states_list: list = ["Info", "Warning", "Error", "Version"]
        if state in states_list:
            self.state = state
        else:
            print(f"Unknown state {state}")
            self.state = state

        self.sys_info = f"[{time.strftime('%X')}] [{self.state}]"

        if self.is_silent_mode:
            pass
        else:
            self.write(f"{self.sys_info} {info}")

        print(f"{self.sys_info} {info}")

    def write(self, text: str):
        if os.path.exists("../log/log.txt"):
            with open("../log/log.txt", "a+") as self.file:
                self.file.write(f"{text}\n")
        else:
            try:
                os.mkdir("../log")
            except FileExistsError:
                pass
            with open("../log/log.txt", "w+") as self.file:
                self.file.write(f"{text}\n")
