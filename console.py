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

    def do_all(self, arg):
        """
         Prints all string representation of all instances based or not on the
         class name.
        """

        instance_rep = []
        if arg:
            if arg not in HBNBCommand.class_names:
                print("** class doesn't exist **")
            else:
                for key in models.storage.all():
                    key_split = key.split(".")
                    if key_split[0] == arg:
                        instance_rep.append(str(models.storage.all()[key]))
                print(instance_rep)
        else:
            for key in models.storage.all():
                instance_rep.append(str(models.storage.all()[key]))
            print(instance_rep)

    def do_update(self, arg):
        """
        Updates an instance based on the class name and id by adding or
        updating attribute (save the change into the JSON file)
        """

        args = arg.split()
        class_name, id, attr_name = args[0], args[1], args[2]
        attr_value = args[3]

        if arg is None or arg == "":
            print("** class name missing **")
            return

        if class_name not in HBNBCommand.class_names:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(class_name, id)
        if key not in models.storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return

        instance = models.storage.all()[key]
        # attr_value = type(attr_name)(attr_value)
        print(f"{attr_name} is of type {type(attr_value)}")
        if isinstance(attr_value, str):
            instance.__dict__[attr_name] = attr_value.replace(
                '"', '').replace("'", '')
        instance.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
