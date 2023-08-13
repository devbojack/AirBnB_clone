#!/usr/bin/python3
"""AirBnB Clone Console."""
import cmd
import models
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
import re
import shlex
from datetime import datetime


class HBNBCommand(cmd.Cmd):
    """Command interpreter
    Attributes:
        prompt: The command prompt.
    """
    prompt = '(hbnb)'
    __clone_classes = [
        "BaseModel",
        "User",
        "City",
        "Place",
        "Review",
        "State",
        "Amenity",
    ]

    def do_quit(self, line):
        """quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """Command to exit the program"""
        return True

    def emptyline(self):
        """Empty line does nothing"""
        pass

    def do_create(self, line):
        """Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id.
        """
        command = self.parseline(line)[0]
        if command is None:
            print('** class name missing **')
        elif command not in self.__clone_classes:
            print("** class doesn't exist **")
        else:
            create_object = eval(command)()
            create_object.save()
            print(create_object.id)

    def do_show(self, line):
        """Prints the string representation of an
        instance based on the class name and id."""
        command = self.parseline(line)[0]
        arg = self.parseline(line)[1]
        if command is None:
            print('** class name missing **')
        elif command not in self.__clone_classes:
            print("** class doesn't exist **")
        elif arg == '':
            print('** instance id missing **')
        else:
            instancedata = models.storage.all().get(command + '.' + arg)
            if instancedata is None:
                print('** no instance found **')
            else:
                print(instancedata)

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id
        (save the change into the JSON file)"""
        command = self.parseline(line)[0]
        args = self.parseline(line)[1]
        if command is None:
            print('** class name missing **')
        elif command not in self.__clone_classes:
            print("** class doesn't exist **")
        elif args == '':
            print('** instance id missing **')
        else:
            k = command + '.' + args
            instancedata = models.storage.all().get(k)
            if instancedata is None:
                print('** no instance found **')
            else:
                del models.storage.all()[k]
                models.storage.save()

    def do_all(self, line):
        """Prints all string representation of all
        instances based or not on the class name.
        """
        command = self.parseline(line)[0]
        objects = models.storage.all()
        if command is None:
            print([str(objects[obj]) for obj in objects])
        elif command in self.__clone_classes:
            keys = objects.keys()
            print([str(objects[k]) for k in keys if k.startswith(command)])
        else:
            print("** class doesn't exist **")

    def do_update(self, line):
        """ Updates an instance based on the class name and id by
        adding or updating attribute (save the change into the JSON file)
        """
        args = shlex.split(line)
        size_args = len(args)
        if size_args == 0:
            print('** class name missing **')
        elif args[0] not in self.__clone_classes:
            print("** class doesn't exist **")
        elif size_args == 1:
            print('** instance id missing **')
        else:
            key = args[0] + '.' + args[1]
            instancedata = models.storage.all().get(key)
            if instancedata is None:
                print('** no instance found **')
            elif size_args == 2:
                print('** attribute name missing **')
            elif size_args == 3:
                print('** value missing **')
            else:
                args[3] = self.value_checker(args[3])
                setattr(instancedata, args[2], args[3])
                setattr(instancedata, 'updated_at', datetime.now())
                models.storage.save()

    def value_checker(self, value):
        """Value checker
        Args:
            value: value to check
        """
        if value.isdigit():
            return int(value)
        elif value.replace('.', '', 1).isdigit():
            return float(value)
        return value

    def default(self, line):
        """Retrieves all instances of a class by
        using: <class name>.all().
        """
        if '.' in line:
            splitted = re.split(r'\.|\(|\)', line)
            class_name = splitted[0]
            method_name = splitted[1]

            if class_name in self.__clone_classes:
                if method_name == 'all':
                    print(self.get_objects(class_name))
                elif method_name == 'count':
                    print(len(self.get_objects(class_name)))
                elif method_name == 'show':
                    class_id = splitted[2][1:-1]
                    self.do_show(class_name + ' ' + class_id)
                elif method_name == 'destroy':
                    class_id = splitted[2][1:-1]
                    self.do_destroy(class_name + ' ' + class_id)

    def get_objects(self, instance=''):
        """Gets the elements created by the console
        Args:
            instance (str): The instance
        Returns:
            list: All instances if available.
        """
        objects = models.storage.all()

        if instance:
            keys = objects.keys()
            return [str(val) for key, val in objects.items()
                    if key.startswith(instance)]

        return [str(val) for key, val in objects.items()]


if __name__ == '__main__':
    HBNBCommand().cmdloop()

