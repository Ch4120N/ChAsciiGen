# -*- coding: UTF-8 -*-
# cli/interactive.py

from __future__ import annotations

import os
import sys
import cmd
import signal
import shlex
import platform
import argparse
import random 

from colorama import Fore, init
init(autoreset=True)

from core.ascii_art import Figlet
from core.config import PROMPT, COMMAND_NOT_FOUND
from core.exception import ChAsciiGenParserExit
from ui.banner import MainBanner, MainSubBanner
from ui.decorators import MsgDCR
from ui.colorize import colorize
from ui.display import CenteredBanner


class Interactive(cmd.Cmd):
    prompt = PROMPT
    _nocmd = COMMAND_NOT_FOUND

    def __init__(self, completekey: str = "tab", stdin = None, stdout = None) -> None:
        super().__init__(completekey, stdin, stdout)
        self._centered_banner = CenteredBanner(clear_screen=False)
        self._figlet = Figlet()

        if (os.name == 'nt' ):
            major_version = int(platform.release())
            if major_version >= 10:
                self._support_colored_prompt = True
                self._readline = True
            else:
                self._support_colored_prompt = False
                self._readline = False
        else:
            self._support_colored_prompt = True
            self._readline = True
        
        if self._support_colored_prompt:
            self.input = input
        else:
            self.input = self._colorized_prompt
        
        self.do_clear('')
    
    def _colorized_prompt(self, *args):
        print(*args, end='', flush=True)
        return input()
    
    def _str_or_int(self, value: str | int) -> str | int:
        try:
            return int(value)
        except ValueError:
            return value
    
    def complete_command_args(self, COMMAND_ARGS, text, line, *_):
        """
        General autocompletion for top-level commands and their arguments.
        """
        try:
            argv = shlex.split(line)
        except ValueError:
            return []

        if not argv:
            return []

        cmd = argv[0]
        arg_index = len(argv) if line.endswith(" ") else len(argv) - 1

        suggestions = COMMAND_ARGS.get(cmd, {}).get(arg_index, [])
        return [s for s in suggestions if s.startswith(text)]


    def emptyline(self) -> None: # type: ignore
        pass
    
    def do_help(self, arg):
        """
        Display a list of available commands or show help for a specific command.

        SYNOPSIS:
            help [command]

        DESCRIPTION:
            The `help` command shows a formatted list of all available commands 
            in the interface. If a command name is provided as an argument, it will 
            display detailed help for that specific command.

            When used without arguments, it lists all known commands with a brief 
            description.

        EXAMPLES:
            help
                Shows a full list of available commands.

            help show
                Displays detailed help for the 'show' command.
        """
        if arg:
            try:
                func = getattr(self, 'help_' + arg)
            except AttributeError:
                try:
                    doc = getattr(self, 'do_' + arg).__doc__
                    if doc:
                        self.stdout.write("%s\n" % str(doc))
                        return
                except AttributeError:
                    pass
                self.stdout.write("%s\n" % str(self.nohelp % (arg,)))
                return
            func()
        else:
            names = self.get_names()
            seen = set()
            commands = []

            for name in names:
                if name.startswith("do_"):
                    cmd_name = name[3:]
                    if cmd_name in seen:
                        continue
                    seen.add(cmd_name)
                    func = getattr(self, name)
                    doc = func.__doc__.strip().split("\n")[0] if func.__doc__ else ""
                    commands.append((cmd_name.upper(), doc))
                elif name.startswith("help_"):
                    cmd_name = name[5:]
                    if cmd_name not in seen:
                        seen.add(cmd_name)
                        commands.append((cmd_name.upper(), ""))
            dic_cmd = []
            for cmd, desc in sorted(commands):
                if desc == '':
                    continue
                dic_cmd.append(colorize("%BoldGreen", f"\t{cmd:<15}:  ", "%BoldWhite", desc, "%Reset"))
            self.do_clear('')
            print('\n'.join(dic_cmd))
            # self.center_text.display(banner())
            # panel = TextPanel(border_color=Fore.LIGHTBLUE_EX)
            # self.center_text.display(panel.build(dic_cmd).splitlines())
            print()
    
    def default(self, line: str) -> None:
        sys.stdout.write(self._nocmd % (line))
    
    def cmdloop(self, intro=None):
        """Repeatedly issue a prompt, accept input, parse an initial prefix
        off the received input, and dispatch to action methods, passing them
        the remainder of the line as argument.

        """

        self.preloop()
        if self._readline:
            if self.use_rawinput and self.completekey:
                try:
                    import readline
                    self.old_completer = readline.get_completer() # type: ignore
                    readline.set_completer(self.complete) # type: ignore
                    readline.parse_and_bind(self.completekey+": complete") # type: ignore
                except ImportError:
                    pass
        try:
            if intro is not None:
                self.intro = intro
            if self.intro:
                self.stdout.write(str(self.intro)+"\n")
            stop = None
            while not stop:
                if self.cmdqueue:
                    line = self.cmdqueue.pop(0)
                else:
                    if self.use_rawinput:
                        try:
                            line = self.input(self.prompt)
                        except EOFError:
                            line = 'EOF'
                        except KeyboardInterrupt:
                            print(f"{Fore.LIGHTRED_EX}Interrupt: use the 'exit' command to quit")
                            line = ''
                    else:
                        self.stdout.write(self.prompt)
                        self.stdout.flush()
                        line = self.stdin.readline()
                        if not len(line):
                            line = 'EOF'
                        else:
                            line = line.rstrip('\r\n')
                line = self.precmd(line)
                stop = self.onecmd(line)
                stop = self.postcmd(stop, line)
            self.postloop()
        finally:
            if self._readline:
                if self.use_rawinput and self.completekey:
                    try:
                        import readline
                        readline.set_completer(self.old_completer) # type: ignore
                    except ImportError:
                        pass

    def do_clear(self, arg):
        """
        Clear the console screen and reset session output

        SYNOPSIS:
            clear

        OPTIONS:
            (none)
                This command takes no arguments or options. Simply invoking `clear`
                will wipe the visible console buffer and redraw a clean prompt.

        DESCRIPTION:
            The `clear` command is used to purge the current console output, effectively
            resetting the visible screen state. This is useful when the console becomes
            cluttered during long sessions, especially when handling large outputs,
            error logs, or verbose module executions.

            The command does not terminate any running modules, sessions, or variables.
            It simply refreshes the interface to improve visual clarity and focus.
            It's a cosmetic command, safe to use at any point.

            It is also helpful in shared terminals or during demonstrations to remove
            sensitive data from view without ending the session.

        EXAMPLES:
            clear
                Clear all text on cli
        """
        
        os.system('cls' 
                  if (os.name == 'nt') else 'clear'
        )
        self._centered_banner.display(MainBanner())
        self._centered_banner.display(MainSubBanner())
    
    def do_exit(self, arg):
        """
        Exit the ChAsciiGen

        SYNOPSIS:
            exit

        DESCRIPTION:
            Terminates the current CHASCIIGEN shell session and exits the framework. This
            command cleanly closes the interactive interface, ensuring no background
            processes remain active. Use this command to safely leave the tool after
            completing operations.
        """

        sys.exit(0)
    
    def do_fonts(self, argv):
        """
        Show full list of all fonts

        SYNOPSIS:
            fonts
        
        DESCRIPTION:
            Displays a full, numbered, and neatly formatted list of all available fonts 
            supported by the pyfiglet library. The fonts are listed in a multi-column,
            terminal-responsive layout to ensure readability regardless of terminal width.
        
        EXAMPLES:
            fonts
                list all available fonts
        """
        self._figlet.showfonts()

    def do_show(self, argv):
        """
        Generate and display ASCII art from input text

        SYNOPSIS:
            show [OPTIONS] <text>

        OPTIONS:
            -f <font name>, --font <font name>
                Use a specific font for rendering. You can list available fonts
                using the `fonts` command.
                Example: -f slant
            
            -r, --random
                Use a random font for rendering the ASCII art.

            -h, --help
                Show this help message for the `show` command.

        DESCRIPTION:
            The `show` command takes input text and converts it into an ASCII art representation. 
            You can optionally specify a font or use a random one.

            If no options are provided, the default font (usually 'standard') will be used.

        EXAMPLES:
            show Hello World
                Display ASCII art for "Hello World" using the default font.

            show -r Hello World
                Display ASCII art for "Hello World" using a randomly selected font.

            show -f slant Hello World
                Display ASCII art for "Hello World" using the 'slant' font.

            show -h
                Show detailed usage information for this command.
        """
        parser = argparse.ArgumentParser(
                    prog="show",
                    description="Generate and display ASCII art from input text",
                    formatter_class=argparse.RawTextHelpFormatter,
                    add_help=False
                )
        parser.add_argument('text', type=str)
        parser.add_argument('-f', '--font', type=str, dest='font')
        parser.add_argument('-r', '--random', action='store_true', dest='random')
        parser.add_argument('-h', '--help', action='store_true', help='Show help message')

        parser.error = lambda message: (
            self.do_help("show") or (_ for _ in ()).throw(ChAsciiGenParserExit(message))
        )

        try:
            args = parser.parse_args(shlex.split(argv))
        except SystemExit:
            MsgDCR.FailureMessage('Invalid syntax. Use `help save` for usage.')
            return
        except Exception as e:
            MsgDCR.FailureMessage(f'Error parsing arguments: {e}')
            return
        
        if args.help:
            self.do_help('show')
            return 
        
        if args.font and args.random:
            MsgDCR.FailureMessage('You cannot use both --font and --random options together.')
            return
        
        font = args.font or 'standard'

        if font:
            print(self._figlet.text2ascii(args.text, font=font))
        
        if args.random:
            selected_font = random.choice(self._figlet._fonts)
            print(self._figlet.text2ascii(args.text, font=selected_font))
    
    def do_save(self, argv):
        """
        Generate and save ASCII art to a file from input text

        SYNOPSIS:
            save [OPTIONS] <text>

        OPTIONS:
            -f <font name>, --font <font name>
                Use a specific font for rendering.
                Example: -f slant

            -r, --random
                Use a random font for rendering the ASCII art.

            -a, --all
                Generate ASCII art using all available fonts and save all to the output file.

            -o <file>, --output <file>
                Specify the output file path. (Required)

            -h, --help
                Show this help message for the `save` command.

        DESCRIPTION:
            The `save` command takes input text and generates ASCII art from it.
            You can save the output to a file using a specified font, a random font, 
            or generate art with all available fonts.

            When using the --all option, ASCII art for all fonts will be concatenated 
            and saved into the specified output file.

        EXAMPLES:
            save -r "Hello World" -o hello.txt
                Save ASCII art of "Hello World" with a random font to hello.txt

            save -f slant "Hello World" -o art.txt
                Save ASCII art of "Hello World" with the 'slant' font to art.txt

            save --all "Test" -o all_fonts.txt
                Save ASCII art for "Test" using all available fonts into all_fonts.txt

            save -h
                Show detailed usage information for this command.
        """
        parser = argparse.ArgumentParser(
            prog="save",
            description="Generate and save ASCII art to a file from input text",
            formatter_class=argparse.RawTextHelpFormatter,
            add_help=False
        )
        parser.add_argument('text', type=str, help='Text to convert and save')
        parser.add_argument('-f', '--font', type=str, dest='font', help='Specify a font to use')
        parser.add_argument('-r', '--random', action='store_true', dest='random', help='Use a random font')
        parser.add_argument('-a', '--all', action='store_true', dest='all_fonts', help='Generate with all available fonts')
        parser.add_argument('-o', '--output', type=str, dest='output', required=True, help='Output file path')
        parser.add_argument('-h', '--help', action='help', help='Show this help message and exit')

        parser.error = lambda message: (
                    self.do_help("save") or (_ for _ in ()).throw(ChAsciiGenParserExit(message))
                )
        try:
            args = parser.parse_args(shlex.split(argv))
        except SystemExit:
            MsgDCR.FailureMessage('Invalid syntax. Use `help save` for usage.')
            return
        except Exception as e:
            MsgDCR.FailureMessage(f'Error parsing arguments: {e}')
            return
        
        if args.help:
            self.do_help('save')
            return
    
        if args.font and args.random:
            MsgDCR.FailureMessage('You cannot use both --font and --random options together.')
            return

        if args.all_fonts and (args.font or args.random):
            MsgDCR.FailureMessage('The --all option cannot be combined with --font or --random.')
            return

        text_input = " ".join(args.text)
        output_path = args.output

        outputs = []

        try:
            if args.all_fonts:
                fonts = self._figlet._fonts
                for font in fonts:
                    art = self._figlet.text2ascii(text_input, font=font)
                    outputs.append(f"### FONT: {font} ###\n{art}\n\n")
            else:
                if args.random:
                    font = random.choice(self._figlet._fonts)
                else:
                    font = args.font or 'standard'
                art = self._figlet.text2ascii(text_input, font=font)
                outputs.append(f"### FONT: {font} ###\n{art}\n")
        except Exception as e:
            MsgDCR.FailureMessage(f"Failed to generate ASCII art: {e}")
            return

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.writelines(outputs)
            MsgDCR.SuccessMessage(f"ASCII art saved successfully to: {output_path}")
        except Exception as e:
            MsgDCR.FailureMessage(f"Error writing to file: {e}")