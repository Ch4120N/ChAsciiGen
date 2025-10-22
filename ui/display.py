# -*- coding: UTF-8 -*-
# ui/display.py

import os
import shutil
import re
import time
from typing import Union, List

from colorama import Fore, init
init(autoreset=True)


class CenteredBanner:
    """A class to display text or ASCII banners centered in the console with color support."""
    
    def __init__(self, clear_screen: bool = True, padding_char: str = " ", color: str = None): # type: ignore
        """
        Initialize the ConsoleBanner class.
        
        Args:
            clear_screen (bool): Whether to clear the console before displaying.
            padding_char (str): Character used for padding (default is space).
            color (str): ANSI color code to apply to text (default is None).
        """
        self.clear_screen = clear_screen
        self.padding_char = padding_char
        self.color = color if color else ""

    def get_console_size(self):
        """
        Get the current console size (width, height).
        
        Returns:
            tuple: (width, height) of the console.
        """
        try:
            size = shutil.get_terminal_size(fallback=(80, 24))
            return size.columns, size.lines
        except Exception:
            return 80, 24  # Fallback size if detection fails

    def strip_ansi_codes(self, text: str) -> str:
        """
        Remove ANSI escape codes from text for accurate length calculation.
        
        Args:
            text (str): Input text containing possible ANSI codes.
        
        Returns:
            str: Text with ANSI codes removed.
        """
        ansi_regex = re.compile(r'\033\[[0-9;]*[mK]')
        return ansi_regex.sub('', text)

    def center_text(self, text: Union[str, List[str]], vertical: bool = False) -> str:
        """
        Center text or ASCII banner in the console with color support.
        
        Args:
            text (Union[str, List[str]]): Single-line text or list of lines (ASCII art).
            vertical (bool): Whether to center vertically as well.
        
        Returns:
            str: Centered text with color ready to display.
        """
        width, height = self.get_console_size()
        lines = text if isinstance(text, list) else text.splitlines()
        if not lines:
            return ""

        # Find the longest line to determine padding
        max_width = max(len(self.strip_ansi_codes(line)) for line in lines)
        if max_width > width:
            max_width = width  # Truncate if text is wider than console

        centered_lines = []
        for line in lines:
            # Remove ANSI codes for length calculation
            clean_line = self.strip_ansi_codes(line)
            if len(clean_line) > width:
                line = line[:width]  # Truncate line if too long
                clean_line = clean_line[:width]
            padding = (width - len(clean_line)) // 2
            # Apply color only to non-padding text
            colored_line = (self.color + line + Fore.RESET) if self.color else line
            centered_line = self.padding_char * padding + colored_line
            centered_line = centered_line.ljust(width, self.padding_char)
            centered_lines.append(centered_line)

        # Vertical centering
        if vertical and len(lines) < height:
            top_padding = (height - len(lines)) // 2
            centered_lines = [self.padding_char * width] * top_padding + centered_lines
            centered_lines += [self.padding_char * width] * (height - len(centered_lines))
        
        return "\n".join(centered_lines)

    def display(self, text, vertical: bool = False, animate: bool = False):
        """
        Display the centered text or ASCII banner in the console with color and animation.
        
        Args:
            text (Union[str, List[str]]): Text or ASCII art to display.
            vertical (bool): Whether to center vertically.
            animate (bool): Whether to add a simple animation effect.
        """
        if self.clear_screen:
            os.system("cls" if os.name == "nt" else "clear")

        centered_text = self.center_text(text, vertical)
        
        if animate:
            for _ in range(3):  # Simple blink animation
                print(centered_text, flush=True)
                time.sleep(0.3)
                if self.clear_screen:
                    os.system("cls" if os.name == "nt" else "clear")
                time.sleep(0.1)
            print(centered_text, flush=True)  # Final display
        else:
            print(centered_text, flush=True)