# -*- coding: UTF-8 -*-
# cli/parser.py

import sys
import argparse

from colorama import Fore, init
init(autoreset=True)

from core.config import (
    SCRIPT_NAME,
    SCRIPT_DESCRIPTION,
    Config
)
from cli.formatter import HelpFormatter


class Parser:
    
    def build_parser(self) -> argparse.Namespace:
        parser = argparse.ArgumentParser(
            prog=SCRIPT_NAME,
            description=SCRIPT_DESCRIPTION,
            formatter_class=HelpFormatter
        )
        parser.add_argument("-f", "--format", type=str,
                            help="format style font for generating Ascii Art (Default: standard)", dest="style_format", default='standard')
        parser.add_argument("-w", "--width", type=int,
                            help="max width of generated Ascii Art (Default: 80)", dest="max_width", default=80)
        parser.add_argument("--interactive", action="store_true",
                            help="Force interactive prompts", dest="interactive")
        parser.add_argument("-v", "--version", action="version", version=f"{Fore.LIGHTCYAN_EX}\n [ {Fore.LIGHTWHITE_EX}*{Fore.LIGHTCYAN_EX} ] {Fore.LIGHTWHITE_EX}%(prog)s{Fore.LIGHTRED_EX} v{__version__}",
                            help="Shows script version and exit", dest="version")
        return parser.parse_args()