# -*- coding: UTF-8 -*-
# cli/parser.py

import sys
import argparse

from colorama import Fore, init
init(autoreset=True)

from core.config import (
    __version__,
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
        parser.add_argument('text', type=str, nargs='?',
                            help='requirment text for generating Ascii Art')
        parser.add_argument("-f", "--font", type=str,
                            help="format style font for generating Ascii Art (Default: standard)", dest="font")
        parser.add_argument("-w", "--width", type=int,
                            help="max width of generated Ascii Art (Default: 80)", dest="width", default=Config.MAX_WIDTH)
        parser.add_argument('-o', '--output', type=str, dest='output')
        parser.add_argument('-l', '--list-all-fonts', action='store_true', dest='list_all_fonts')
        parser.add_argument('-r', '--random', action='store_true', dest='random')
        parser.add_argument('-a', '--all-fonts', action='store_true', dest='all_fonts')
        parser.add_argument('-s', '--search-font', type=str, dest='search_font')
        parser.add_argument("--interactive", action="store_true",
                            help="Force interactive prompts", dest="interactive")
        parser.add_argument("-v", "--version", action="version", version=f"{Fore.LIGHTCYAN_EX}\n [ {Fore.LIGHTWHITE_EX}*{Fore.LIGHTCYAN_EX} ] {Fore.LIGHTWHITE_EX}%(prog)s{Fore.LIGHTRED_EX} v{__version__}",
                            help="Shows script version and exit", dest="version")
        return parser.parse_args()