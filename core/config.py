# -*- coding: UTF-8 -*-
# core/config.py

from colorama import Fore, init
init(autoreset=True)


__version__ = '1.0'

SCRIPT_NAME = 'ChAsciiGen'

SCRIPT_DESCRIPTION = 'Simple tool for text to ASCII Art generator'

PROMPT = (
    Fore.LIGHTRED_EX + ' root' +
    Fore.LIGHTWHITE_EX + '@' +
    Fore.LIGHTBLUE_EX + 'ChAsciiGen' +
    Fore.LIGHTWHITE_EX + ' :' +
    Fore.LIGHTBLUE_EX + '~' +
    Fore.LIGHTRED_EX + '# '
)
class Config:
    MAX_WIDTH: int = 80
    DEFAULT_FONT: str = 'standard'

