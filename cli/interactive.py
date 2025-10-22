# -*- coding: UTF-8 -*-
# cli/interactive.py

from __future__ import annotations

import cmd
import sys
import signal




class Interactive(cmd.Cmd):
    prompt = 'root@ChAsciiGen :~# '
    def __init__(self, completekey: str = "tab", stdin = None, stdout = None) -> None:
        super().__init__(completekey, stdin, stdout)
    
    def emptyline(self) -> bool:
        return True
    
    def do_list_fonts(self, args):
        print('Fonts: standard')