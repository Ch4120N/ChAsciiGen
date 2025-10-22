# -*- coding: UTF-8 -*-
# cli/interactive.py

from __future__ import annotations

import os
import sys
import cmd
import signal
import shlex
import platform

from colorama import Fore, init
init(autoreset=True)

from ui.banner import MainBanner




class Interactive(cmd.Cmd):
    prompt = 'root@ChAsciiGen :~# '

    def __init__(self, completekey: str = "tab", stdin = None, stdout = None) -> None:
        super().__init__(completekey, stdin, stdout)

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
        MainBanner()
    
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
        pass

    def do_preview(self, argv):
        pass


