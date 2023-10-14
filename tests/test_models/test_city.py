#!/usr/bin/env python3
"""All test for city class"""
import unittest
import os
import json
from datetime import datetime
from models.city import City
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class Testcity(unittest.TestCase):
    """Testcase class definition(inherits from unittest.TestCase)"""

    def test_is_subclass(self):
        """Test that city is a subclass of BaseModel"""
        city = City()
        self.assertIsInstance(city, BaseModel)
        self.assertTrue(hasattr(city, "id"))
        self.assertTrue(hasattr(city, "created_at"))
        self.assertTrue(hasattr(city, "updated_at"))

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
        """Test city class initialization"""

        my_city = City()
        self.assertEqual(my_city.name, "")
        self.assertEqual(my_city.state_id, "")
        my_city.name = "Abeokuta"
        my_city.state_id = "12121"

        self.assertIsInstance(my_city, City)
        self.assertIsInstance(my_city.name, str)
        self.assertIsInstance(my_city.id, str)
        self.assertIsInstance(my_city.state_id, str)
        self.assertIsInstance(my_city.created_at, datetime)
        self.assertIsInstance(my_city.updated_at, datetime)

        self.assertEqual(my_city.name, "Abeokuta")
        self.assertEqual(my_city.state_id, "12121")

    def test_city_str(self):
        """Test magic str format"""

        my_city = City()
        magic_str = f"[City] ({my_city.id}) {my_city.__dict__}"
        self.assertEqual(str(my_city), magic_str)

    def test_city_save(self):
        """Test for save method"""

        my_city = City()
        current_time = my_city.updated_at
        my_city.save()
        self.assertNotEqual(current_time, my_city.updated_at)

    def test_city_to_dict(self):
        """Test to_dict method"""

        my_city = City()
        my_city.name = "Abeokuta"
        my_city.state_id = "12121"
        my_city_json = my_city.to_dict()

        self.assertIsInstance(my_city_json, dict)
        self.assertEqual(my_city_json["name"], my_city.name)
        self.assertEqual(my_city_json["id"], my_city.id)
        self.assertEqual(my_city_json["state_id"], my_city.state_id)
        self.assertEqual(my_city_json["__class__"], "City")
        self.assertEqual(my_city_json["created_at"]
                         [:-7], my_city.created_at.isoformat()[:-7])
        self.assertEqual(my_city_json["updated_at"]
                         [:-7], my_city.updated_at.isoformat()[:-7])

    def test_to_dict_data_type(self):
        """Test to check if instance is json compatible"""

        my_city = City()
        my_city.name = "Abeokuta"
        my_city.state_id = "12121"
        my_city_json = my_city.to_dict()

        self.assertIsInstance(my_city_json["name"], str)
        self.assertIsInstance(my_city_json["id"], str)
        self.assertIsInstance(my_city_json["state_id"], str)
        self.assertIsInstance(my_city_json["__class__"], str)
        self.assertIsInstance(my_city_json["created_at"], str)
        self.assertIsInstance(my_city_json["updated_at"], str)

    def test_city_kwargs_initialization(self):
        """Test for when kwargs is passed as city param"""

        my_city = City()
        my_city.name = "Abeokuta"
        my_city.state_id = "12121"
        my_city_json = my_city.to_dict()
        my_new_city = City(**my_city_json)

        self.assertNotEqual(my_new_city.created_at,
                            my_city_json["created_at"])
        self.assertNotEqual(my_new_city.updated_at,
                            my_city_json["updated_at"])
        self.assertEqual(my_new_city.name, my_city_json["name"])
        self.assertEqual(my_new_city.state_id, my_city_json["state_id"])
        self.assertEqual(my_new_city.id, my_city_json["id"])
        self.assertFalse(my_city is my_new_city)

    def test_new(self):
        """Test to check new() method behaviour"""
        obj = City()
        self.storage.new(obj)
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.assertIn(key, self.storage.all())

    def test_save(self):
        """Test to check save() method behaviour"""
        obj = City()
        self.storage.new(obj)
        self.storage.save()
        self.assertTrue(os.path.exists(self.file_path))
        key = f"{obj.__class__.__name__}.{obj.id}"
        with open(self.file_path) as f:
            data = json.load(f)
        self.assertIn(key, data)

    def test_reload(self):
        """Test to check reload() method behaviour"""
        obj = City()
        self.storage.new(obj)
        self.storage.save()
        self.storage._FileStorage__objects = {}
        self.storage.reload()
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.assertIn(key, self.storage.all())

    def test_instance_deletion(self):
        """Test for behaviour after destroying an instance"""
        obj = City()
        self.storage.new(obj)
        self.storage.save()
        obj_key = f"{obj.__class__.__name__}.{obj.id}"
        del obj
        self.storage.reload()
        self.storage._FileStorage__objects.clear()
        self.assertNotIn(obj_key, self.storage.all())

    def test_instance_diff(self):
        """Test inequality of two BaseModel Instance"""

        my_city = City()
        my_city1 = City()

        self.assertNotEqual(my_city, my_city1)


if __name__ == "__main__":
    unittest.main()
