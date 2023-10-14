#!/usr/bin/python3
"""Test defines tests for amenity.py"""

import unittest
from models.state import State
from models.base_model import BaseModel
# from models import storage


class TestAmenity(unittest.TestCase):
    """test for the amenity class"""

    def test_is_subclass(self):
        """Test that State is a subclass of BaseModel"""
        state = State()
        self.assertIsInstance(state, BaseModel)
        self.assertTrue(hasattr(state, "id"))
        self.assertTrue(hasattr(state, "created_at"))
        self.assertTrue(hasattr(state, "updated_at"))

    def setUp(self):
        """set up the class"""
        self.state = State()

    def test_attribute_initialization(self):
        """test if class initializes"""
        self.assertEqual(self.state.name, "")

    def test_attribute_types(self):
        """test if attribute name is a string"""
        self.assertIsInstance(self.state.name, str)

    def test_name_attr(self):
        """Test that State has attribute name"""
        state = State()
        self.assertTrue(hasattr(state, "name"))
        self.assertEqual(state.name, "")

    def test_attribute_values(self):
        """test if the values are set correctly"""
        self.state.name = "Enugu"

        self.assertEqual(self.state.name, "Enugu")

    def test_update_attribute_values(self):
        """test if values update correctly"""
        self.state.name = "Nigeria"

        self.assertEqual(self.state.name, "Nigeria")


if __name__ == '__main__':
    unittest.main()
