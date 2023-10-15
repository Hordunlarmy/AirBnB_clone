#!/usr/bin/env python3
"""
 A class FileStorage that serializes instances to a JSON file and deserializes
 JSON file to instances:
"""
import json
# import os
from models.base_model import BaseModel  # noqa
from models.user import User  # noqa
from models.state import State  # noqa
from models.city import City  # noqa
from models.amenity import Amenity  # noqa
from models.place import Place  # noqa
from models.review import Review  # noqa


class FileStorage:
    """The birth of FileStorage"""

    __file_path = "file.json"
    __objects = {}
    class_names = {"BaseModel", "User", "State", "City", "Amenity", "Place",
                   "Review"}

    def all(self):
        """returns the dictionary __objects"""

        return FileStorage.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""

        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """ serializes __objects to the JSON file (path: __file_path)"""

        obj_dict = {}
        for key in FileStorage.__objects:
            obj_dict[key] = FileStorage.__objects[key].to_dict()

        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(obj_dict, f, indent=2)

    def reload(self):
        """
        deserializes the JSON file to __objects (only if the JSON file
        (__file_path) exists ; otherwise, do nothing. If the file doesn’t
        exist, no exception should be raised)
        """

        # if os.path.isfile(FileStorage.__file_path):
        try:
            with open(FileStorage.__file_path) as f:
                obj_dict = json.load(f)
                for key, value in obj_dict.items():
                    class_name = value['__class__']
                    my_class = eval(class_name)
                    obj_instance = my_class(**value)

                    FileStorage.__objects[key] = obj_instance
        except FileNotFoundError:
            return
