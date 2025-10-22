# -*- coding: UTF-8 -*-
# ui/colorize.py

import re
import difflib

from colorama import Fore, Back, Style, init
init(autoreset=True)


ANSI = {
    "reset": Style.RESET_ALL,     # reset everything
    "bold": Style.BRIGHT,      # bold/bright style
    "dim": "\x1b[2;3m",     # dim or italic style
    "lined": "\x1b[4m",     # underline
    "blink": "\x1b[5m",     # blinking style
    "invert": "\x1b[7m",    # invert Fore/Back
    "basic": Style.NORMAL,    # set normal style
    # Foreground COLOR CODES
    "black": Fore.BLACK,    # black color
    "red": Fore.RED,      # red color
    "green": Fore.GREEN,    # green color
    "yellow": Fore.YELLOW,   # yellow color
    "blue": Fore.BLUE,     # blue color
    "magenta": Fore.MAGENTA,  # magenta color
    "cyan": Fore.CYAN,     # cyan color
    "white": Fore.WHITE,    # white color
    "normal": Fore.RESET,   # default Fore color
    
    # Back COLOR CODES
    "bgblack": Back.LIGHTBLACK_EX,  # black Back
    "bgred": Back.RED,    # red Back
    "bggreen": Back.GREEN,  # green Back
    "bgyellow": Back.GREEN, # yellow Back
    "bgblue": Back.BLUE,   # blue Back
    "bgpink": Back.MAGENTA,   # pink/magenta Back
    "bgcyan": Back.CYAN,   # cyan Back
    "bgmagenta": Back.MAGENTA,
    "bgwhite": Back.WHITE,  # white Back
    "bgnormal": Back.RESET  # default Back color
    
}

def colorize(*args):
    """Takes single or multiple strings as argument, and colorize them.

    Syntax:
      * Ansi color/style can be defined by providing a CamelCase
        formatted color code that starts with '%' and can contain
        multiple codes.
        For example: "%BoldYellow" will return "\\x1b[1m\\x1b[33m".
        Back colors can be specified with 'Bg' prefix, e.g., "%BgBlue".
      * Any string that does not strictly match the syntax above is
        left as it is.

    Behavior:
      * If at least one of the provided arguments is a standard string
        (aka non-ANSI color code), then the result will be a
        concatenation of all the arguments, with formatted ANSI codes.
      * If the last argument is a standard string, and at least one
        argument was a color code, an ANSI reset is automatically added
        to its end.
      * If multiple arguments are given, and all of them are ANSI color
        codes, a tuple for each is then returned instead of a
        concatenated result string.

    Examples:
    >>> colorize('%DimPink', 'Hello ', '%Bold', 'world !')
    '\\x1b[2;3mHello \\x1b[1mworld !\\x1b[0m'
    >>> colorize('%DimBlack', '%BgWhite', 'root ● ChDosRipper ►► ')
    '\\x1b[2;3m\\x1b[30m\\x1b[47mroot ● ChDosRipper ►► \\x1b[0m'
    >>> colorize('%BgBlue', '%Yellow', 'Hello')
    '\\x1b[44m\\x1b[33mHello\\x1b[0m'
    >>> colorize('%Invert', '%BgWhite')
    ('\\x1b[7m', '\\x1b[47m')
    >>> colorize('Hello world !')
    'Hello world !'
    """
    colors = 0  # the number of color code args
    strings = 0  # the number of standard string args
    result = []  # the final result

    for idx, arg in enumerate(args):
        arg = str(arg)
        # Check if the argument is an ANSI color code (starts with %)
        if arg.startswith('%'):
            # Remove the % and split into CamelCase parts
            code = arg[1:]
            # Try to match the entire code or combinations like BgWhite
            split = []
            if code.lower() in ANSI:
                split = [code.lower()]
            else:
                # Split into parts, but handle BgColor combinations
                parts = re.findall(r'[A-Z][a-z]+', code)
                i = 0
                while i < len(parts):
                    # Check for BgColor combination
                    if i + 1 < len(parts) and parts[i].lower() == 'bg':
                        split.append(f'bg{parts[i+1].lower()}')
                        i += 2
                    else:
                        split.append(parts[i].lower())
                        i += 1

            # If all parts are valid ANSI codes
            if all(c in ANSI for c in split):
                # Add the corresponding ANSI codes
                result.append(''.join(ANSI[c] for c in split))
                colors += 1
                continue

        # If the arg is a standard string
        # If it's the last arg, and at least one color was set, auto-add reset
        if colors >= 1 and idx == len(args) - 1:
            arg += ANSI['reset']
        result.append(arg)
        strings += 1

    # Single or absent argument returns a string in all cases
    if len(result) < 2:
        return ''.join(result)

    # If only colors were requested, return a tuple of them
    if not strings:
        return tuple(result)

    # Else return a concatenated string
    return ''.join(result)

def decolorize(string):
    """Returns a colorless version of the given string.
    Based on a regular expression that removes any standard ANSI code.

    Example:
    >>> decolorize('string \\x1b[2m\\x1b[32mcolor !\\x1b[0m')
    'string color !'
    """
    regex = "\x01?\x1b\\[((?:\\d|;)*)([a-zA-Z])\x02?"
    return re.sub(regex, "", str(string))

def diff(old, new, display=True):
    """Nice colored diff implementation
    """
    if not isinstance(old, list):
        old = decolorize(str(old)).splitlines()
    if not isinstance(new, list):
        new = decolorize(str(new)).splitlines()

    line_types = {' ': '%Reset', '-': '%Red', '+': '%Green', '?': '%Pink'}

    if display:
        for line in difflib.Differ().compare(old, new):
            if line.startswith('?'):
                continue
            print(colorize(line_types[line[0]], line))

    return old != new