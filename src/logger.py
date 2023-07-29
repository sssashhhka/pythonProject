import time
import os
from typing import Literal

version: str = "Logger v.3.0"


def log(info: str, state: Literal["Info", "Warning", "Error", "Version"] = "Info", silent: bool = False):
    current_time: str = time.strftime("%d:%m:%Y %X")
    output: str = f"[{current_time}] [{state}] {info}\n"
    if silent:
        pass
    else:
        if os.path.exists("log/log.txt"):
            with open("log/log.txt", "a") as f:
                f.write(output)
        else:
            try:
                os.mkdir("log")
            except FileExistsError:
                pass
            with open("log/log.txt", "w") as f:
                f.write(output)
    output = f"[{current_time}] [{state}] {info}"
    print(output)
