# -*- coding: UTF-8 -*-
# core/config.py

from colorama import Fore, init
init(autoreset=True)

from ui.colorize import colorize


__version__ = '1.0'

SCRIPT_NAME = 'ChAsciiGen'

SCRIPT_DESCRIPTION = 'Simple tool for text to ASCII Art generator'

PROMPT = str(colorize(
    '%BoldRed', 'root',
    '%BoldWhite', '@',
    '%BoldBlue', 'ChAsciiGen',
    '%BoldRed', ' ~# '
))

COMMAND_NOT_FOUND = f"{Fore.LIGHTRED_EX}{SCRIPT_NAME} {Fore.LIGHTWHITE_EX}: command {Fore.LIGHTRED_EX}'%s'{Fore.LIGHTWHITE_EX} not found.\n"

class Config:
    MAX_WIDTH: int = 80
    DEFAULT_FONT: str = 'standard'

