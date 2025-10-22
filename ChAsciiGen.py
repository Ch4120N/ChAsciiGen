# -*- coding: UTF-8 -*-
# ChAsciiGen.py

import sys

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
        'If you are using the Linux operating system, you must install the required libraries globally using the package manager\n'
        'Or create a virtual environment and then install the required libraries.\n'
    )

from ui.banner import MainBanner
from ui.decorators import MsgDCR
from cli.parser import Parser

class ChAsciiGen:
    def __init__(self):
        self.parser = Parser()

    def run(self):
        MainBanner()
        args = self.parser.build_parser()

        if args.interactive:
            MsgDCR.FailureMessage('Currently interactive mode is disabled!')
            sys.exit(2)


if __name__ == '__main__':
    app = ChAsciiGen()
    sys.exit(app.run())