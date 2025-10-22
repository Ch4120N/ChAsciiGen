# -*- coding: UTF-8 -*-
# ui/decorators.py

from colorama import Fore, Style, init
init(autoreset=True)


class StatusDecorator:
    def __init__(self):
        self.PASS = Style.BRIGHT + Fore.GREEN + \
            "[ " + Style.BRIGHT + Fore.WHITE + "+" + \
            Style.BRIGHT + Fore.GREEN + " ] " + Style.RESET_ALL
        self.FAIL = Style.BRIGHT + Fore.RED + \
            "[ " + Style.BRIGHT + Fore.WHITE + "-" + \
            Style.BRIGHT + Fore.RED + " ] " + Style.RESET_ALL
        self.WARN = Style.BRIGHT + Fore.YELLOW + \
            "[ " + Style.BRIGHT + Fore.WHITE + "!" + \
            Style.BRIGHT + Fore.YELLOW + " ] " + Style.RESET_ALL
        self.HEAD = Style.BRIGHT + Fore.CYAN + \
            "[ " + Style.BRIGHT + Fore.WHITE + "::" + \
            Style.BRIGHT + Fore.CYAN + " ] " + Style.RESET_ALL
        self.INFO = Style.BRIGHT + Fore.CYAN + \
            "[ " + Style.BRIGHT + Fore.WHITE + "*" + \
            Style.BRIGHT + Fore.CYAN + " ] " + Style.RESET_ALL
        self.STDS = "           "

class MessageDecorator(StatusDecorator):
    def InfoMessage(self, RequestMessage):
        print(self.INFO + Style.BRIGHT + Fore.WHITE + RequestMessage + Style.RESET_ALL)
    
    def SuccessMessage(self, RequestMessage):
        print(self.PASS + Style.BRIGHT + Fore.GREEN + RequestMessage + Style.RESET_ALL)

    def FailureMessage(self, RequestMessage):
        print(self.FAIL + Style.BRIGHT + Fore.RED + RequestMessage + Style.RESET_ALL)

    def WarningMessage(self, RequestMessage):
        print(self.WARN + Style.BRIGHT + Fore.YELLOW + RequestMessage + Style.RESET_ALL)

    def SectionMessage(self, RequestMessage):
        print(self.HEAD + Style.BRIGHT + Fore.CYAN + RequestMessage + Style.RESET_ALL)

    def GeneralMessage(self, RequestMessage):
        print(self.STDS + Style.RESET_ALL + RequestMessage)

MsgDCR = MessageDecorator()