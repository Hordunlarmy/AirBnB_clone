#!/usr/bin/env python3
"""All test for state class"""
import unittest
import os
import json
from datetime import datetime
from models.state import State
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class Teststate(unittest.TestCase):
    """Testcase class definition(inherits from unittest.TestCase)"""

    def test_is_subclass(self):
        """Test that State is a subclass of BaseModel"""
        state = State()
        self.assertIsInstance(state, BaseModel)
        self.assertTrue(hasattr(state, "id"))
        self.assertTrue(hasattr(state, "created_at"))
        self.assertTrue(hasattr(state, "updated_at"))

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
        """Test state class initialization"""

        my_state = State()
        self.assertEqual(my_state.name, "")
        my_state.name = "Abeokuta"

        self.assertIsInstance(my_state, State)
        self.assertIsInstance(my_state.name, str)
        self.assertIsInstance(my_state.id, str)
        self.assertEqual(len(my_state.id), 36)
        self.assertIsInstance(my_state.created_at, datetime)
        self.assertIsInstance(my_state.updated_at, datetime)

        self.assertEqual(my_state.name, "Abeokuta")

    def test_state_str(self):
        """Test magic str format"""

        my_state = State()
        magic_str = f"[State] ({my_state.id}) {my_state.__dict__}"
        self.assertEqual(str(my_state), magic_str)

    def test_state_save(self):
        """Test for save method"""

        my_state = State()
        current_time = my_state.updated_at
        my_state.save()
        self.assertNotEqual(current_time, my_state.updated_at)

    def test_state_to_dict(self):
        """Test to_dict method"""

        my_state = State()
        my_state.name = "Abeokuta"
        my_state_json = my_state.to_dict()

        self.assertIsInstance(my_state_json, dict)
        self.assertEqual(my_state_json["name"], my_state.name)
        self.assertEqual(my_state_json["id"], my_state.id)
        self.assertEqual(my_state_json["__class__"], "State")
        self.assertEqual(my_state_json["created_at"]
                         [:-7], my_state.created_at.isoformat()[:-7])
        self.assertEqual(my_state_json["updated_at"]
                         [:-7], my_state.updated_at.isoformat()[:-7])

    def test_to_dict_data_type(self):
        """Test to check if instance is json compatible"""

        my_state = State()
        my_state.name = "Abeokuta"
        my_state_json = my_state.to_dict()

        self.assertIsInstance(my_state_json["name"], str)
        self.assertIsInstance(my_state_json["id"], str)
        self.assertIsInstance(my_state_json["__class__"], str)
        self.assertIsInstance(my_state_json["created_at"], str)
        self.assertIsInstance(my_state_json["updated_at"], str)

    def test_state_kwargs_initialization(self):
        """Test for when kwargs is passed as state param"""

        my_state = State()
        my_state.name = "Abeokuta"
        my_state_json = my_state.to_dict()
        my_new_state = State(**my_state_json)

        self.assertNotEqual(my_new_state.created_at,
                            my_state_json["created_at"])
        self.assertNotEqual(my_new_state.updated_at,
                            my_state_json["updated_at"])
        self.assertEqual(my_new_state.name, my_state_json["name"])
        self.assertEqual(my_new_state.id, my_state_json["id"])
        self.assertFalse(my_state is my_new_state)

    def test_new(self):
        """Test to check new() method behaviour"""
        obj = State()
        self.storage.new(obj)
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.assertIn(key, self.storage.all())

    def test_save(self):
        """Test to check save() method behaviour"""
        obj = State()
        self.storage.new(obj)
        self.storage.save()
        self.assertTrue(os.path.exists(self.file_path))
        key = f"{obj.__class__.__name__}.{obj.id}"
        with open(self.file_path) as f:
            data = json.load(f)
        self.assertIn(key, data)

    def test_reload(self):
        """Test to check reload() method behaviour"""
        obj = State()
        self.storage.new(obj)
        self.storage.save()
        self.storage._FileStorage__objects = {}
        self.storage.reload()
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.assertIn(key, self.storage.all())

    def test_instance_deletion(self):
        """Test for behaviour after destroying an instance"""
        obj = State()
        self.storage.new(obj)
        self.storage.save()
        obj_key = f"{obj.__class__.__name__}.{obj.id}"
        del obj
        self.storage.reload()
        self.storage._FileStorage__objects.clear()
        self.assertNotIn(obj_key, self.storage.all())

    def test_instance_diff(self):
        """Test inequality of two BaseModel Instance"""

        my_state = State()
        my_state1 = State()

        self.assertNotEqual(my_state, my_state1)


if __name__ == "__main__":
    unittest.main()
