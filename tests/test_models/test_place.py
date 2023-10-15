#!/usr/bin/env python3
"""All test for place class"""
import unittest
import os
import json
from datetime import datetime
from models.place import Place
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestPlace(unittest.TestCase):
    """Testcase class definition(inherits from unittest.TestCase)"""

    def test_is_subclass(self):
        """Test that place is a subclass of BaseModel"""
        place = Place()
        self.assertIsInstance(place, BaseModel)
        self.assertTrue(hasattr(place, "id"))
        self.assertTrue(hasattr(place, "created_at"))
        self.assertTrue(hasattr(place, "updated_at"))

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
        """Test place class initialization"""

        my_place = Place()
        self.assertEqual(my_place.name, "")
        self.assertEqual(my_place.city_id, "")
        self.assertEqual(my_place.user_id, "")
        self.assertEqual(my_place.description, "")
        self.assertEqual(my_place.number_rooms, 0)
        self.assertEqual(my_place.number_bathrooms, 0)
        self.assertEqual(my_place.max_guest, 0)
        self.assertEqual(my_place.price_by_night, 0)
        self.assertEqual(my_place.latitude, 0.0)
        self.assertEqual(my_place.longitude, 0.0)
        self.assertEqual(my_place.amenity_ids, [])
        my_place.name = "Good"
        my_place.city_id = "12121"
        my_place.user_id = "10000"

        self.assertIsInstance(my_place, Place)
        self.assertIsInstance(my_place.name, str)
        self.assertIsInstance(my_place.id, str)
        self.assertIsInstance(my_place.city_id, str)
        self.assertIsInstance(my_place.created_at, datetime)
        self.assertIsInstance(my_place.updated_at, datetime)

        self.assertEqual(my_place.name, "Good")
        self.assertEqual(my_place.city_id, "12121")
        self.assertEqual(my_place.user_id, "10000")

    def test_place_str(self):
        """Test magic str format"""

        my_place = Place()
        magic_str = f"[Place] ({my_place.id}) {my_place.__dict__}"
        self.assertEqual(str(my_place), magic_str)

    def test_place_save(self):
        """Test for save method"""

        my_place = Place()
        current_time = my_place.updated_at
        my_place.save()
        self.assertNotEqual(current_time, my_place.updated_at)

    def test_place_to_dict(self):
        """Test to_dict method"""

        my_place = Place()
        my_place.name = "Good"
        my_place.city_id = "12121"
        my_place.user_id = "10000"
        my_place_json = my_place.to_dict()

        self.assertIsInstance(my_place_json, dict)
        self.assertEqual(my_place_json["name"], my_place.name)
        self.assertEqual(my_place_json["id"], my_place.id)
        self.assertEqual(my_place_json["city_id"], my_place.city_id)
        self.assertEqual(my_place_json["__class__"], "Place")
        self.assertEqual(my_place_json["created_at"]
                         [:-7], my_place.created_at.isoformat()[:-7])
        self.assertEqual(my_place_json["updated_at"]
                         [:-7], my_place.updated_at.isoformat()[:-7])

    def test_to_dict_data_type(self):
        """Test to check if instance is json compatible"""

        my_place = Place()
        my_place.name = "Good"
        my_place.city_id = "12121"
        my_place.user_id = "10000"
        my_place_json = my_place.to_dict()

        self.assertIsInstance(my_place_json["name"], str)
        self.assertIsInstance(my_place_json["id"], str)
        self.assertIsInstance(my_place_json["city_id"], str)
        self.assertIsInstance(my_place_json["__class__"], str)
        self.assertIsInstance(my_place_json["created_at"], str)
        self.assertIsInstance(my_place_json["updated_at"], str)

    def test_place_kwargs_initialization(self):
        """Test for when kwargs is passed as place param"""

        my_place = Place()
        my_place.name = "Good"
        my_place.city_id = "12121"
        my_place.user_id = "10000"
        my_place_json = my_place.to_dict()
        my_new_place = Place(**my_place_json)

        self.assertNotEqual(my_new_place.created_at,
                            my_place_json["created_at"])
        self.assertNotEqual(my_new_place.updated_at,
                            my_place_json["updated_at"])
        self.assertEqual(my_new_place.name, my_place_json["name"])
        self.assertEqual(my_new_place.city_id, my_place_json["city_id"])
        self.assertEqual(my_new_place.id, my_place_json["id"])
        self.assertFalse(my_place is my_new_place)

    def test_new(self):
        """Test to check new() method behaviour"""
        obj = Place()
        self.storage.new(obj)
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.assertIn(key, self.storage.all())

    def test_save(self):
        """Test to check save() method behaviour"""
        obj = Place()
        self.storage.new(obj)
        self.storage.save()
        self.assertTrue(os.path.exists(self.file_path))
        key = f"{obj.__class__.__name__}.{obj.id}"
        with open(self.file_path) as f:
            data = json.load(f)
        self.assertIn(key, data)

    def test_reload(self):
        """Test to check reload() method behaviour"""
        obj = Place()
        self.storage.new(obj)
        self.storage.save()
        self.storage._FileStorage__objects = {}
        self.storage.reload()
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.assertIn(key, self.storage.all())

    def test_instance_deletion(self):
        """Test for behaviour after destroying an instance"""
        obj = Place()
        self.storage.new(obj)
        self.storage.save()
        obj_key = f"{obj.__class__.__name__}.{obj.id}"
        del obj
        self.storage.reload()
        self.storage._FileStorage__objects.clear()
        self.assertNotIn(obj_key, self.storage.all())

    def test_instance_diff(self):
        """Test inequality of two BaseModel Instance"""

        my_place = Place()
        my_place1 = Place()

        self.assertNotEqual(my_place, my_place1)


if __name__ == "__main__":
    unittest.main()
