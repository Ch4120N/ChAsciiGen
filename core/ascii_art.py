# -*- coding: UTF-8 -*-
# core/ascii_art.py

from __future__ import annotations

import shutil
import re

from pyfiglet import FigletFont, figlet_format
from colorama import Fore, init
init(autoreset=True)

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
    
    def text2ascii(self, text:str, font: str = 'standard', width: int = 80):
        if font.isdigit():
            font_number = int(font)
            if 1 <= font_number <= self._total_fonts:
                selected_font = self._fonts[font_number - 1]
            else:
                MsgDCR.FailureMessage('Invalid number! Please enter valid font number.')
                return ''
        else:
            if font in self._fonts:
                selected_font = font
            else:
                MsgDCR.FailureMessage('Invalid font name! Please enter valid font name.')
                return ''
        
        return str(figlet_format(text, font=selected_font, width=width))

    def highlight(self, keyword: str, text:str):
        i = 0
        result = ""
        while i < len(text):
            if text[i:i+len(keyword)].lower() == keyword.lower():
                result += Fore.RED + text[i:i+len(keyword)] + Fore.RESET
                i += len(keyword)
            else:
                result += text[i]
                i += 1
        return result

    def strip_ansi_codes(self, text: str) -> str:
        ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
        return ansi_escape.sub('', text)

    def serach_font(self, keyword: str):
        filtered_fonts = [font for font in self._fonts if keyword.lower() in font.lower()]
        
        if not filtered_fonts:
            MsgDCR.WarningMessage(f"No fonts found containing keyword: {Fore.LIGHTWHITE_EX}'{Fore.LIGHTRED_EX}{keyword}{Fore.LIGHTWHITE_EX}'")
            return

        numbered_fonts_raw = [f"{i+1}. {font}" for i, font in enumerate(filtered_fonts)]
        max_len = max(len(self.strip_ansi_codes(item)) for item in numbered_fonts_raw) + 4
        cols = max(1, self._term_width // max_len)
        rows = (len(numbered_fonts_raw) + cols - 1) // cols
        highlighted_fonts = [self.highlight(keyword, item) for item in numbered_fonts_raw]

        output_lines = []
        for row in range(rows):
            line = ''
            for col in range(cols):
                idx = row * cols + col
                if idx < len(highlighted_fonts):
                    item = highlighted_fonts[idx]
                    padding = max_len - len(self.strip_ansi_codes(item))
                    line += item + ' ' * padding
            output_lines.append('    ' + line)

        print('\n'.join(output_lines))
        print()