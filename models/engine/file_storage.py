#!/usr/bin/env python3
"""
 A class FileStorage that serializes instances to a JSON file and deserializes
 JSON file to instances:
"""
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """The birth of FileStorage"""

    __file_path = "file.json"
    __objects = {}

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

        if os.path.isfile(FileStorage.__file_path):
            with open(FileStorage.__file_path) as f:
                obj_dict = json.load(f)
                for key, value in obj_dict.items():
                    class_name = value['__class__']
                    if class_name == 'BaseModel':
                        obj_instance = BaseModel(**value)
                    if class_name == 'User':
                        obj_instance = User(**value)
                    if class_name == 'State':
                        obj_instance = State(**value)
                    if class_name == 'City':
                        obj_instance = City(**value)
                    if class_name == 'Amenity':
                        obj_instance = Amenity(**value)
                    if class_name == 'Place':
                        obj_instance = Place(**value)
                    if class_name == 'Review':
                        obj_instance = Review(**value)

                    FileStorage.__objects[key] = obj_instance
