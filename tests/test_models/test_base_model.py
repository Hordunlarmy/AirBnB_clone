#!/usr/bin/env python3
"""All test for BaseModel class"""
import unittest
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Testcase class definition(inherits from unittest.TestCase)"""

    def test_init(self):
        """Test class initialization"""

        my_model = BaseModel()
        my_model.name = "My First Model"
        my_model.my_number = 89

        self.assertIsInstance(my_model, BaseModel)
        self.assertIsInstance(my_model.name, str)
        self.assertIsInstance(my_model.my_number, int)
        self.assertIsInstance(my_model.id, str)
        self.assertEqual(len(my_model.id), 36)
        self.assertIsInstance(my_model.created_at, datetime)
        self.assertIsInstance(my_model.updated_at, datetime)

    def test_str(self):
        """Test magic str format"""

        my_model = BaseModel()
        magic_str = f"[BaseModel] ({my_model.id}) {my_model.__dict__}"
        self.assertEqual(str(my_model), magic_str)

    def test_save(self):
        """Test for save method"""

        my_model = BaseModel()
        current_time = my_model.updated_at
        my_model.save()

        self.assertNotEqual(current_time, my_model.updated_at)

    def test_to_dict(self):
        """Test to_dict method"""

        my_model = BaseModel()
        my_model.name = "My First Model"
        my_model.my_number = 89
        my_model_json = my_model.to_dict()

        self.assertIsInstance(my_model_json, dict)
        self.assertEqual(my_model_json["name"], my_model.name)
        self.assertEqual(my_model_json["my_number"], my_model.my_number)
        self.assertEqual(my_model_json["id"], my_model.id)
        self.assertEqual(my_model_json["__class__"], "BaseModel")
        self.assertEqual(my_model_json["created_at"]
                         [:-7], my_model.created_at.isoformat()[:-7])
        self.assertEqual(my_model_json["updated_at"]
                         [:-7], my_model.updated_at.isoformat()[:-7])

    def test_to_dict_data_type(self):
        """Test to check if instance is json compatible"""

        my_model = BaseModel()
        my_model.name = "My First Model"
        my_model.my_number = 89
        my_model_json = my_model.to_dict()

        self.assertIsInstance(my_model_json["name"], str)
        self.assertIsInstance(my_model_json["my_number"], int)
        self.assertIsInstance(my_model_json["id"], str)
        self.assertIsInstance(my_model_json["__class__"], str)
        self.assertIsInstance(my_model_json["created_at"], str)
        self.assertIsInstance(my_model_json["updated_at"], str)

    def test_kwargs_initialization(self):
        """Test for when kwargs is passed as BaseModel param"""

        my_model = BaseModel()
        my_model.name = "My_First_Model"
        my_model.my_number = 89
        my_model_json = my_model.to_dict()
        my_new_model = BaseModel(**my_model_json)

        self.assertNotEqual(my_new_model.created_at,
                            my_model_json["created_at"])
        self.assertNotEqual(my_new_model.updated_at,
                            my_model_json["updated_at"])
        self.assertEqual(my_new_model.my_number, my_model_json["my_number"])
        self.assertEqual(my_new_model.name, my_model_json["name"])
        self.assertEqual(my_new_model.id, my_model_json["id"])
        self.assertFalse(my_model is my_new_model)

    def test_instance_diff(self):
        """Test inequality of two BaseModel Instance"""

        my_model = BaseModel()
        my_model1 = BaseModel()

        self.assertNotEqual(my_model, my_model1)


if __name__ == "__main__":
    unittest.main()
