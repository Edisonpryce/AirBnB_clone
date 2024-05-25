#!/usr/bin/python3
"""Entry point of command interpreter"""

import cmd
import re
import json
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """contains the entry point of the command interpreter"""

    prompt = '(hbnb) '
    __classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

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

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            new_instance = HBNBCommand.__classes[args[0]]()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, arg):
        """Prints the string representation of an instance based on the
        class name and id
        """
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        key = f"{args[0]}.{args[1]}"
        instance = storage.all().get(key)
        if instance is None:
            print("** no instance found **")
        else:
            print(instance)

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        key = f"{args[0]}.{args[1]}"
        if key in storage.all():
            del storage.all()[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representation of all instances based or
        not on the class name"""
        args = arg.split()
        if len(args) == 0:
            instances = [str(obj) for obj in storage.all().values()]
            print(instances)
        else:
            if args[0] not in HBNBCommand.__classes:
                print("** class doesn't exist **")
                return
            instances = [str(obj) for key, obj in storage.all().items()
                         if key.startswith(args[0])]
            print(instances)

    def do_update(self, arg):
        """Updates an instance based on the class name and id by
        adding or updating attribute
        """
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return

        class_name, instance_id, attr_name, attr_value = (args[0], args[1],
                                                          args[2], args[3])
        key = f"{class_name}.{instance_id}"
        instance = storage.all().get(key)

        if instance is None:
            print("** no instance found **")
            return

        if attr_name in ["id", "created_at", "updated_at"]:
            print("** attribute cannot be updated **")
            return
        if attr_value.isdigit():
            attr_value = int(attr_value)
        else:
            try:
                attr_value = float(attr_value)
            except ValueError:
                pass

        setattr(instance, attr_name, attr_value)
        instance.save()

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "count": self.do_count,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update
        }
        match = re.search(r"^(\w+)\.(\w+)\((.*)\)$", arg)
        if match:
            class_name, method, params = match.groups()
            if class_name in HBNBCommand.__classes and method in argdict:
                if method == "update":
                    params_match = re.match(r'\"(.*?)\", (\{.*\})', params)
                    if params_match:
                        instance_id, dict_attrs = params_match.groups()
                        try:
                            dict_attrs = json.loads(dict_attrs.replace
                                                    ("'", '"'))
                        except json.JSONDecodeError:
                            print("** invalid dictionary format **")
                            return
                        for attr_name, attr_value in dict_attrs.items():
                            command = (f"{class_name} {instance_id} "
                                       f"({attr_name} {attr_value}")
                            self.do_update(command)
                        return
                    params_match = re.match(r'\"(.*?)\", \"(.*?)\", (.+)',
                                            params)
                    if params_match:
                        instance_id, attr_name, attr_value = (
                            params_match.groups())
                        command = (f"{class_name} {instance_id} "
                                   f"{attr_name} {attr_value}")
                        argdict[method](command)
                        return
                else:
                    params = params.strip('"')
                    command = f"{class_name} {params}"
                    argdict[method](command)
                    return
        print("*** Unknown syntax: {}".format(arg))

    def do_count(self, arg):
        """Counts the number of instances of a class"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        count = sum(1 for key in storage.all().keys()
                    if key.startswith(args[0]))
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
