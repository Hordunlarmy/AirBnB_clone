#!/usr/bin/env python3
"""All test for FileStorage class"""
import os
import json
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class TestFileStorage(unittest.TestCase):
    """Filestorage class definition(inherits from unittest.TestCase)"""

    def setUp(self):
        """Set up for the tests"""

        self.file_path = "test_file.json"
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        FileStorage._FileStorage__file_path = self.file_path
        self.storage = FileStorage()
        self.storage.reload()

    def tearDown(self):
        """Clear file after each test"""

        try:
            if os.path.exists(self.file_path):
                os.remove(self.file_path)
        except Exception as e:
            print(f"Error occurred while deleting file: {e}")

    def test_filestorage_instance(self):
        """Test instances and types for Filestorage"""

        self.assertEqual(FileStorage, type(FileStorage()))
        self.assertEqual(type(FileStorage._FileStorage__file_path), str)
        self.assertEqual(type(FileStorage._FileStorage__objects), dict)

    def test_all_returns_dictionary(self):
        """Test to check if all() returns a dictionary"""
        self.assertIsInstance(self.storage.all(), dict)

    def test_new(self):
        """Test to check new() method behaviour"""

        obj = BaseModel()
        self.storage.new(obj)
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.assertIn(key, self.storage.all())

    def test_save_time(self):
        """Test to check if time gets updated after save"""

        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()
        self.assertEqual(obj.updated_at, datetime.now())

    def test_save(self):
        """Test to check save() method behaviour"""

        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()
        self.assertTrue(os.path.exists(self.file_path))
        key = f"{obj.__class__.__name__}.{obj.id}"
        with open(self.file_path) as f:
            data = json.load(f)
        self.assertIn(key, data)

    def test_reload(self):
        """Test to check reload() method behaviour"""

        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()
        self.storage._FileStorage__objects = {}
        self.storage.reload()
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.assertIn(key, self.storage.all())

    def test_all_empty_storage(self):
        """Test all command on empty file"""

        all_objs = self.storage.all()
        for obj_id in all_objs.keys():
            obj = all_objs[obj_id]
            self.assertIsNotNone(obj)
        self.assertTrue(os.path.isfile('file.json'))

    def test_reload_with_arg(self):
        """Test to check reload() method behaviour with an argument"""

        with self.assertRaises(TypeError):
            self.storage.reload(None)

    def test_reload_without_arg(self):
        """Test to check reload() method behaviour without arguments"""

        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()
        self.storage._FileStorage__objects = {}
        self.storage.reload()
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.assertIn(key, self.storage.all())

    def test_reload_from_file(self):
        """Test reloading from JSON file"""

        objs = self.storage.all()
        for obj in objs.values():
            self.assertIsNotNone(obj)
            self.assertTrue(isinstance(
                obj, (BaseModel, User, State, City, Amenity, Place, Review)))
        self.assertTrue(os.path.isfile('file.json'))

    def test_instance_deletion(self):
        """Test for behaviour after destroying an instance"""

        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()
        obj_key = f"{obj.__class__.__name__}.{obj.id}"
        del obj
        self.storage.reload()
        self.storage._FileStorage__objects.clear()
        self.assertNotIn(obj_key, self.storage.all())

    def test_new_multiple_objects(self):
        """Test creating and saving all objects"""

        obj1 = BaseModel()
        obj2 = User()
        obj3 = State()
        obj4 = City()
        obj5 = Amenity()
        obj6 = Place()
        obj7 = Review()
        self.storage.new(obj1)
        self.storage.new(obj2)
        self.storage.new(obj3)
        self.storage.new(obj4)
        self.storage.new(obj5)
        self.storage.new(obj6)
        self.storage.new(obj7)
        self.storage.save()
        obj1_key = f"{obj1.__class__.__name__}.{obj1.id}"
        obj2_key = f"{obj2.__class__.__name__}.{obj2.id}"
        obj3_key = f"{obj3.__class__.__name__}.{obj3.id}"
        obj4_key = f"{obj4.__class__.__name__}.{obj4.id}"
        obj5_key = f"{obj5.__class__.__name__}.{obj5.id}"
        obj6_key = f"{obj6.__class__.__name__}.{obj6.id}"
        obj7_key = f"{obj7.__class__.__name__}.{obj7.id}"
        self.storage._FileStorage__objects = {}
        self.storage.reload()
        self.assertIn(obj1_key, self.storage.all())
        self.assertIn(obj2_key, self.storage.all())
        self.assertIn(obj3_key, self.storage.all())
        self.assertIn(obj4_key, self.storage.all())
        self.assertIn(obj5_key, self.storage.all())
        self.assertIn(obj6_key, self.storage.all())
        self.assertIn(obj7_key, self.storage.all())


if __name__ == "__main__":
    unittest.main()
