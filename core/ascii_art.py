# -*- coding: UTF-8 -*-
# core/ascii_art.py

from __future__ import annotations

import shutil

from pyfiglet import FigletFont, figlet_format

from ui.decorators import MsgDCR


class Figlet:
    def __init__(self) -> None:
        self._fonts = FigletFont.getFonts()
        self._total_fonts = len(self._fonts)
        self._term_width = shutil.get_terminal_size().columns
    
    def showfonts(self) -> None:
        numbered_fonts = [f"{i+1}. {font}" for i, font in enumerate(self._fonts)]
        max_len = max(len(item) for item in numbered_fonts) + 2
        cols = max(1, self._term_width // max_len)
        rows = [numbered_fonts[i:i+cols] for i in range(0, len(numbered_fonts), cols)]
        fonts = []

        for row in rows:
            line = ""
            for item in row:
                line += item.ljust(max_len)
            fonts.append((' '*4) + line)
        
        print('\n'.join(fonts))
        print()
    
    def text2ascii(self, text:str, font: str = 'standard'):
        if font.isdigit():
            font_number = int(font)
            if 1 <= font_number <= self._total_fonts:
                selected_font = self._fonts[font_number - 1]
            else:
                MsgDCR.FailureMessage('Invalid number! Please enter valid font number.')
                return
        else:
            if font in self._fonts:
                selected_font = font
            else:
                MsgDCR.FailureMessage('Invalid font name! Please enter valid font name.')
                return
        
        return str(figlet_format(text, font=selected_font))