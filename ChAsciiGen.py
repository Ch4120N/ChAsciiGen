# -*- coding: UTF-8 -*-
# ChAsciiGen.py

import sys

try:
    import pyfiglet
    from colorama import Fore, init
    init(autoreset=True)
except ImportError:
    sys.exit(
        '[ - ] Please install the required libraries. Use the following commands to install:\n'
        '\t - python -m pip install colorama pyfiglet pyreadline3\n'
        '\t OR\n'
        '\t - python -m pip install -r requirements.txt\n\n'
        'If you are using the Linux operating system, you must install the required libraries globally using the package manager\n'
        'Or create a virtual environment and then install the required libraries.\n'
    )
