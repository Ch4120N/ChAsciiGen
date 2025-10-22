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

from colorama import Fore, init
init(autoreset=True)

from core.ascii_art import figlet
from core.config import PROMPT, COMMAND_NOT_FOUND
from ui.banner import MainBanner, MainSubBanner
from ui.colorize import colorize
from ui.display import CenteredBanner


class Interactive(cmd.Cmd):
    prompt = PROMPT
    _nocmd = COMMAND_NOT_FOUND

    def __init__(self, completekey: str = "tab", stdin = None, stdout = None) -> None:
        super().__init__(completekey, stdin, stdout)
        self._centered_banner = CenteredBanner(clear_screen=False)

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

            help list
                Displays detailed help for the 'support' command.
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
    
    def do_list(self, argv):
        args = argv.split()

        if args[0] == 'fonts':
            figlet.showfonts()

    def do_preview(self, argv):
        pass


