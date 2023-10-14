#!/usr/bin/env python3
"""All test for amenity class"""
import unittest
import os
import json
from datetime import datetime
from models.amenity import Amenity
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class Testamenity(unittest.TestCase):
    """Testcase class definition(inherits from unittest.TestCase)"""

    def test_is_subclass(self):
        """Test that amenity is a subclass of BaseModel"""
        amenity = Amenity()
        self.assertIsInstance(amenity, BaseModel)
        self.assertTrue(hasattr(amenity, "id"))
        self.assertTrue(hasattr(amenity, "created_at"))
        self.assertTrue(hasattr(amenity, "updated_at"))

    def setUp(self):
        """Set up for the tests"""
        self.file_path = "test_file.json"
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

    def test_init(self):
        """Test amenity class initialization"""

        my_amenity = Amenity()
        self.assertEqual(my_amenity.name, "")
        my_amenity.name = "Abeokuta"

        self.assertIsInstance(my_amenity, Amenity)
        self.assertIsInstance(my_amenity.name, str)
        self.assertIsInstance(my_amenity.id, str)
        self.assertEqual(len(my_amenity.id), 36)
        self.assertIsInstance(my_amenity.created_at, datetime)
        self.assertIsInstance(my_amenity.updated_at, datetime)

        self.assertEqual(my_amenity.name, "Abeokuta")

    def test_amenity_str(self):
        """Test magic str format"""

        my_amenity = Amenity()
        magic_str = f"[Amenity] ({my_amenity.id}) {my_amenity.__dict__}"
        self.assertEqual(str(my_amenity), magic_str)

    def test_amenity_save(self):
        """Test for save method"""

        my_amenity = Amenity()
        current_time = my_amenity.updated_at
        my_amenity.save()
        self.assertNotEqual(current_time, my_amenity.updated_at)

    def test_amenity_to_dict(self):
        """Test to_dict method"""

        my_amenity = Amenity()
        my_amenity.name = "Abeokuta"
        my_amenity_json = my_amenity.to_dict()

        self.assertIsInstance(my_amenity_json, dict)
        self.assertEqual(my_amenity_json["name"], my_amenity.name)
        self.assertEqual(my_amenity_json["id"], my_amenity.id)
        self.assertEqual(my_amenity_json["__class__"], "Amenity")
        self.assertEqual(my_amenity_json["created_at"]
                         [:-7], my_amenity.created_at.isoformat()[:-7])
        self.assertEqual(my_amenity_json["updated_at"]
                         [:-7], my_amenity.updated_at.isoformat()[:-7])

    def test_to_dict_data_type(self):
        """Test to check if instance is json compatible"""

        my_amenity = Amenity()
        my_amenity.name = "Abeokuta"
        my_amenity_json = my_amenity.to_dict()

        self.assertIsInstance(my_amenity_json["name"], str)
        self.assertIsInstance(my_amenity_json["id"], str)
        self.assertIsInstance(my_amenity_json["__class__"], str)
        self.assertIsInstance(my_amenity_json["created_at"], str)
        self.assertIsInstance(my_amenity_json["updated_at"], str)

    def test_amenity_kwargs_initialization(self):
        """Test for when kwargs is passed as amenity param"""

        my_amenity = Amenity()
        my_amenity.name = "Abeokuta"
        my_amenity_json = my_amenity.to_dict()
        my_new_amenity = Amenity(**my_amenity_json)

        self.assertNotEqual(my_new_amenity.created_at,
                            my_amenity_json["created_at"])
        self.assertNotEqual(my_new_amenity.updated_at,
                            my_amenity_json["updated_at"])
        self.assertEqual(my_new_amenity.name, my_amenity_json["name"])
        self.assertEqual(my_new_amenity.id, my_amenity_json["id"])
        self.assertFalse(my_amenity is my_new_amenity)

    def test_new(self):
        """Test to check new() method behaviour"""
        obj = Amenity()
        self.storage.new(obj)
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.assertIn(key, self.storage.all())

    def test_save(self):
        """Test to check save() method behaviour"""
        obj = Amenity()
        self.storage.new(obj)
        self.storage.save()
        self.assertTrue(os.path.exists(self.file_path))
        key = f"{obj.__class__.__name__}.{obj.id}"
        with open(self.file_path) as f:
            data = json.load(f)
        self.assertIn(key, data)

    def test_reload(self):
        """Test to check reload() method behaviour"""
        obj = Amenity()
        self.storage.new(obj)
        self.storage.save()
        self.storage._FileStorage__objects = {}
        self.storage.reload()
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.assertIn(key, self.storage.all())

    def test_instance_deletion(self):
        """Test for behaviour after destroying an instance"""
        obj = Amenity()
        self.storage.new(obj)
        self.storage.save()
        obj_key = f"{obj.__class__.__name__}.{obj.id}"
        del obj
        self.storage.reload()
        self.storage._FileStorage__objects.clear()
        self.assertNotIn(obj_key, self.storage.all())

    def test_instance_diff(self):
        """Test inequality of two BaseModel Instance"""

        my_amenity = Amenity()
        my_amenity1 = Amenity()

        self.assertNotEqual(my_amenity, my_amenity1)


if __name__ == "__main__":
    unittest.main()
