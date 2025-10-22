# -*- coding: UTF-8 -*-
# core/ascii_art.py

import shutil

from pyfiglet import FigletFont



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
