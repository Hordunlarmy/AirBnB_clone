#!/usr/bin/env python3
import cmd


class HBNBCommand(cmd.Cmd):
    """Class definition"""

    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Exit the program"""
        return True

    def do_EOF(self, arg):
        """Handle EOF (Ctrl+D) to exit"""
        return True

    def help_quit(self):
        """Change help message for the quit command"""
        print("Quit command to exit the program\n")

    def default(self, line):
        """Called on an unrecognized command"""
        if not line:
            return
    def emptyline(self):
        """Do nothing on empty input line"""
        pass


if __name__ == "__main__":
    HBNBCommand().cmdloop()
