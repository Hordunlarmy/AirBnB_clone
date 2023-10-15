#!/usr/bin/env python3
"""All test for User class"""
import unittest
import os
import json
from datetime import datetime
from models.user import User
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestUser(unittest.TestCase):
    """Testcase class definition(inherits from unittest.TestCase)"""

    def test_is_subclass(self):
        """Test that State is a subclass of BaseModel"""
        user = User()
        self.assertIsInstance(user, BaseModel)
        self.assertTrue(hasattr(user, "id"))
        self.assertTrue(hasattr(user, "created_at"))
        self.assertTrue(hasattr(user, "updated_at"))

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

    def test_init_without_add_attribute(self):
        """Test initialization without adding new attribute"""

        my_user = User()
        self.assertEqual(my_user.first_name, "")
        self.assertEqual(my_user.last_name, "")
        self.assertEqual(my_user.email, "")
        self.assertEqual(my_user.password, "")

    def test_init(self):
        """Test User class initialization with new attribute"""

        my_user = User()
        my_user.first_name = "Betty"
        my_user.last_name = "Bar"
        my_user.email = "airbnb@mail.com"
        my_user.password = "root"

        self.assertIsInstance(my_user, User)
        self.assertIsInstance(my_user.email, str)
        self.assertIsInstance(my_user.password, str)
        self.assertIsInstance(my_user.first_name, str)
        self.assertIsInstance(my_user.last_name, str)
        self.assertIsInstance(my_user.id, str)
        self.assertEqual(len(my_user.id), 36)
        self.assertIsInstance(my_user.created_at, datetime)
        self.assertIsInstance(my_user.updated_at, datetime)

        self.assertEqual(my_user.first_name, "Betty")
        self.assertEqual(my_user.last_name, "Bar")
        self.assertEqual(my_user.email, "airbnb@mail.com")
        self.assertEqual(my_user.password, "root")

    def test_user_str(self):
        """Test magic str format"""

        my_user = User()
        magic_str = f"[User] ({my_user.id}) {my_user.__dict__}"
        self.assertEqual(str(my_user), magic_str)

    def test_user_save(self):
        """Test for save method"""

        my_user = User()
        current_time = my_user.updated_at
        my_user.save()
        self.assertNotEqual(current_time, my_user.updated_at)

    def test_user_to_dict(self):
        """Test to_dict method"""

        my_user = User()
        my_user.first_name = "Betty"
        my_user.last_name = "Bar"
        my_user.email = "airbnb@mail.com"
        my_user.password = "root"
        my_user_json = my_user.to_dict()

        self.assertIsInstance(my_user_json, dict)
        self.assertEqual(my_user_json["first_name"], my_user.first_name)
        self.assertEqual(my_user_json["last_name"], my_user.last_name)
        self.assertEqual(my_user_json["email"], my_user.email)
        self.assertEqual(my_user_json["password"], my_user.password)
        self.assertEqual(my_user_json["id"], my_user.id)
        self.assertEqual(my_user_json["__class__"], "User")
        self.assertEqual(my_user_json["created_at"]
                         [:-7], my_user.created_at.isoformat()[:-7])
        self.assertEqual(my_user_json["updated_at"]
                         [:-7], my_user.updated_at.isoformat()[:-7])

    def test_to_dict_data_type(self):
        """Test to check if instance is json compatible"""

        my_user = User()
        my_user.first_name = "Betty"
        my_user.last_name = "Bar"
        my_user.email = "airbnb@mail.com"
        my_user.password = "root"
        my_user_json = my_user.to_dict()

        self.assertIsInstance(my_user_json["first_name"], str)
        self.assertIsInstance(my_user_json["last_name"], str)
        self.assertIsInstance(my_user_json["email"], str)
        self.assertIsInstance(my_user_json["password"], str)
        self.assertIsInstance(my_user_json["id"], str)
        self.assertIsInstance(my_user_json["__class__"], str)
        self.assertIsInstance(my_user_json["created_at"], str)
        self.assertIsInstance(my_user_json["updated_at"], str)

    def test_user_kwargs_initialization(self):
        """Test for when kwargs is passed as User param"""

        my_user = User()
        my_user.first_name = "Betty"
        my_user.last_name = "Bar"
        my_user.email = "airbnb@mail.com"
        my_user.password = "root"
        my_user_json = my_user.to_dict()
        my_new_user = User(**my_user_json)

        self.assertNotEqual(my_new_user.created_at,
                            my_user_json["created_at"])
        self.assertNotEqual(my_new_user.updated_at,
                            my_user_json["updated_at"])
        self.assertEqual(my_new_user.first_name, my_user_json["first_name"])
        self.assertEqual(my_new_user.last_name, my_user_json["last_name"])
        self.assertEqual(my_new_user.email, my_user_json["email"])
        self.assertEqual(my_new_user.password, my_user_json["password"])
        self.assertEqual(my_new_user.id, my_user_json["id"])
        self.assertFalse(my_user is my_new_user)

    def test_new(self):
        """Test to check new() method behaviour"""
        obj = User()
        self.storage.new(obj)
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.assertIn(key, self.storage.all())

    def test_save(self):
        """Test to check save() method behaviour"""
        obj = User()
        self.storage.new(obj)
        self.storage.save()
        self.assertTrue(os.path.exists(self.file_path))
        key = f"{obj.__class__.__name__}.{obj.id}"
        with open(self.file_path) as f:
            data = json.load(f)
        self.assertIn(key, data)

    def test_reload(self):
        """Test to check reload() method behaviour"""
        obj = User()
        self.storage.new(obj)
        self.storage.save()
        self.storage._FileStorage__objects = {}
        self.storage.reload()
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.assertIn(key, self.storage.all())

    def test_instance_deletion(self):
        """Test for behaviour after destroying an instance"""
        obj = User()
        self.storage.new(obj)
        self.storage.save()
        obj_key = f"{obj.__class__.__name__}.{obj.id}"
        del obj
        self.storage.reload()
        self.storage._FileStorage__objects.clear()
        self.assertNotIn(obj_key, self.storage.all())

    def test_instance_diff(self):
        """Test inequality of two BaseModel Instance"""

        my_user = User()
        my_user1 = User()

        self.assertNotEqual(my_user, my_user1)


if __name__ == "__main__":
    unittest.main()
