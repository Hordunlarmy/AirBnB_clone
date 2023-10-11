#!/usr/bin/env python3
import cmd
import models
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """Class definition"""

    prompt = "(hbnb) "

    class_names = ["BaseModel", "User", "State", "City", "Amenity", "Place",
                   "Review"]

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
        """Called on an empty command"""
        if not line:
            return

    def emptyline(self):
        """Do nothing on empty input line"""
        pass

    def do_create(self, arg):
        """
         Creates a new instance of BaseModel, saves it (to the JSON file) and
         prints the id
        """
        if arg is None or arg == "":
            print("** class name missing **")
        elif arg not in HBNBCommand.class_names:
            print("** class doesn't exist **")
        else:
            new_obj = BaseModel()
            new_obj.save()
            print(new_obj.id)

    def do_show(self, arg):
        """
        Prints the string representation of an instance based on the class
        name and id
        """
        args = arg.split()

        if arg is None or arg == "":
            print("** class name missing **")
        elif args[0] not in HBNBCommand.class_names:
            print("** class doesn't exist **")
        else:
            if len(args) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(args[0], args[1])
                if key not in models.storage.all():
                    print("** no instance found **")
                else:
                    print(models.storage.all()[key])

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id
        (save the change into the JSON file)
        """
        args = arg.split()

        if arg is None or arg == "":
            print("** class name missing **")
        elif args[0] not in HBNBCommand.class_names:
            print("** class doesn't exist **")
        else:
            if len(args) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(args[0], args[1])
                if key not in models.storage.all():
                    print("** no instance found **")
                else:
                    del models.storage.all()[key]
                    models.storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
