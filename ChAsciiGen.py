# -*- coding: UTF-8 -*-
# ChAsciiGen.py

"""
Author     : Ch4120N
GitHub     : GitHub.Com/Ch4120N
Repository : GitHub.Com/Ch4120N/ChAsciiGen
"""

# MIT License

# Copyright (c) 2025 Ch4120N

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import sys
import random

try:
    import pyfiglet
    from colorama import Fore, init
    init(autoreset=True)
except ImportError:
    sys.exit(
        '[ - ] Please install the required libraries. Use the following commands to install:\n\n'
        '\t- python -m pip install colorama pyfiglet pyreadline3\n'
        '\tOR\n'
        '\t- python -m pip install -r requirements.txt\n\n'
        'If you are using Linux, install the required libraries globally using your package manager\n'
        'or create a virtual environment and install them inside it.\n'
    )

# Internal imports
from ui.banner import MainBanner
from ui.decorators import MsgDCR
from cli.parser import Parser
from cli.interactive import Interactive
from core.ascii_art import Figlet
from core.config import Config
from core.io import IO


class ChAsciiGen:
    def __init__(self):
        self.parser = Parser()
        self.interactive = Interactive()
        self.figlet = Figlet()
        self._temp_str = ''

    def run(self):
        config = IO.load_config()
        Config.MAX_WIDTH = config.get('max_width', Config.MAX_WIDTH)
        Config.OUTPUT_FILE = config.get('output_file', Config.OUTPUT_FILE)
        Config.DEFAULT_FONT = config.get('default_font', Config.DEFAULT_FONT)
        Config.CONFIG_FILE = config.get('config_file', Config.CONFIG_FILE)

        """Main method: handles command-line arguments and executes corresponding actions."""
        args = self.parser.build_parser()

        # --- List all available fonts ---
        if getattr(args, 'list_all_fonts', False):
            MsgDCR.InfoMessage(
                f'Available fonts {Fore.LIGHTBLUE_EX}'
                f'({Fore.LIGHTWHITE_EX}{self.figlet._total_fonts}{Fore.LIGHTBLUE_EX})'
                f'{Fore.LIGHTWHITE_EX}:\n'
            )
            self.figlet.showfonts(margin_left=0)
            return 0

        # --- Search for a specific font ---
        search_font = getattr(args, 'search_font', None)
        if search_font:
            # Fixed typo: 'serach_font' -> 'search_font'
            self.figlet.search_font(search_font, 0, True)
            return 0

        # --- Handle conflicting options ---
        font_opt = getattr(args, 'font', None)
        random_opt = getattr(args, 'random', False)
        if font_opt and random_opt:
            MsgDCR.FailureMessage('You cannot use both --font and --random options together.')
            return 1

        # --- Handle output file option ---
        output_file = getattr(args, 'output', None)
        if output_file:
            Config.OUTPUT_FILE = output_file

        # --- Retrieve text and width values ---
        text = getattr(args, 'text')
        width = getattr(args, 'width', 100)
        all_fonts = getattr(args, 'all_fonts', False)
        interactive_mode = getattr(args, 'interactive', False)

        # --- Start interactive mode if no text provided ---
        if not text and not interactive_mode:
            MsgDCR.WarningMessage('No text provided. Starting interactive mode...')
            self.interactive.run()
            return 0

        # --- Handle "--all-fonts" mode ---
        if text and all_fonts:
            if not output_file:
                MsgDCR.WarningMessage('You need to use --output with --all-fonts option.')
                return 1

            outputs = []
            for f in self.figlet._fonts:
                art = self.figlet.text2ascii(text, font=f, width=width)
                outputs.append(f"--- FONT: {f} ---\n{art}\n\n")

            IO.save_writelines_file(outputs)
            return 0

        # --- Determine which font to use ---
        if random_opt:
            font = random.choice(self.figlet._fonts)
            ascii_art = f'--- FONT: {font} ---\n\n' + self.figlet.text2ascii(text, font=font, width=width)
        else:
            font = font_opt or Config.DEFAULT_FONT
            ascii_art = self.figlet.text2ascii(text, font=font, width=width)

        self._temp_str = ascii_art

        # --- Save or print the result ---
        if output_file:
            IO.save_file(self._temp_str)
        else:
            print(self._temp_str)
            return 0

        # --- Fallback to interactive mode if requested ---
        if interactive_mode:
            self.interactive.run()
            return 0


if __name__ == '__main__':
    app = ChAsciiGen()
    sys.exit(app.run())
