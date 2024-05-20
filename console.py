#!/usr/bin/python3
"""Entry point of command interpreter"""

import cmd


class HBNBCommand(cmd.Cmd):
    """contains the entry point of the command interpreter"""

    prompt = '(hbnb) '

    def do_quit(self, arg):
        """Quit command to exit program"""
        return True

    def do_EOF(self, arg):
        """End of file to exit program command"""
        print()
        return True

    def emptyline(self):
        """Do nothing"""
        pass

    def do_help(self, arg):
        """List available commands with help"""
        super().do_help(arg)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
