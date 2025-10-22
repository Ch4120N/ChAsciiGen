# -*- coding: UTF-8 -*-
# ui/banner.py

from colorama import Fore, init
init(autoreset=True)

def MainBanner() -> str:
    return (
        f"{Fore.LIGHTRED_EX}    ___ _       _            _ _   ___           "
        f"{Fore.LIGHTRED_EX}   / __\\ |__   /_\\  ___  ___(_|_) / _ \\___ _ __  "
        f"{Fore.LIGHTRED_EX}  / /  | '_ \\ //_\\/ __|/ __| | |/ /_\\/ _ \\ '_ \\ "
        f"{Fore.LIGHTRED_EX} / /___| | | /  _  \\__ \\ (__| | / /_\\  __/ | | |"
        f"{Fore.LIGHTRED_EX} \\____/|_| |_\\_/ \\_/___/\\___|_|_\\____/\\___|_| |_|"
        f' {Fore.YELLOW}╔═════════════════════════════════════════════╗'
        f' {Fore.YELLOW}║                 {Fore.LIGHTCYAN_EX}ChAsciiGen                  {Fore.YELLOW}║'
        f' {Fore.YELLOW}║{Fore.LIGHTWHITE_EX} Simple tool for text to ASCII Art generator {Fore.YELLOW}║'
        f' {Fore.YELLOW}║ {Fore.LIGHTGREEN_EX}Author  {Fore.LIGHTWHITE_EX}:  {Fore.LIGHTRED_EX}Ch4120N                          {Fore.YELLOW}║'
        f' {Fore.YELLOW}║ {Fore.LIGHTGREEN_EX}Github  {Fore.LIGHTWHITE_EX}:  {Fore.LIGHTRED_EX}Github.com/Ch4120N               {Fore.YELLOW}║'
        f' {Fore.YELLOW}╚═════════════════════════════════════════════╝'
    )