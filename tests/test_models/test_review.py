#!/usr/bin/env python3
"""All test for review class"""
import unittest
import os
import json
from datetime import datetime
from models.review import Review
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestReview(unittest.TestCase):
    """Testcase class definition(inherits from unittest.TestCase)"""

    def test_is_subclass(self):
        """Test that review is a subclass of BaseModel"""
        review = Review()
        self.assertIsInstance(review, BaseModel)
        self.assertTrue(hasattr(review, "id"))
        self.assertTrue(hasattr(review, "created_at"))
        self.assertTrue(hasattr(review, "updated_at"))

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
        """Test review class initialization"""

        my_review = Review()
        self.assertEqual(my_review.text, "")
        self.assertEqual(my_review.place_id, "")
        self.assertEqual(my_review.user_id, "")
        my_review.text = "Good"
        my_review.place_id = "12121"
        my_review.user_id = "10000"

        self.assertIsInstance(my_review, Review)
        self.assertIsInstance(my_review.text, str)
        self.assertIsInstance(my_review.id, str)
        self.assertIsInstance(my_review.place_id, str)
        self.assertIsInstance(my_review.created_at, datetime)
        self.assertIsInstance(my_review.updated_at, datetime)

        self.assertEqual(my_review.text, "Good")
        self.assertEqual(my_review.place_id, "12121")
        self.assertEqual(my_review.user_id, "10000")

    def test_review_str(self):
        """Test magic str format"""

        my_review = Review()
        magic_str = f"[Review] ({my_review.id}) {my_review.__dict__}"
        self.assertEqual(str(my_review), magic_str)

    def test_review_save(self):
        """Test for save method"""

        my_review = Review()
        current_time = my_review.updated_at
        my_review.save()
        self.assertNotEqual(current_time, my_review.updated_at)

    def test_review_to_dict(self):
        """Test to_dict method"""

        my_review = Review()
        my_review.text = "Good"
        my_review.place_id = "12121"
        my_review.user_id = "10000"
        my_review_json = my_review.to_dict()

        self.assertIsInstance(my_review_json, dict)
        self.assertEqual(my_review_json["text"], my_review.text)
        self.assertEqual(my_review_json["id"], my_review.id)
        self.assertEqual(my_review_json["place_id"], my_review.place_id)
        self.assertEqual(my_review_json["__class__"], "Review")
        self.assertEqual(my_review_json["created_at"]
                         [:-7], my_review.created_at.isoformat()[:-7])
        self.assertEqual(my_review_json["updated_at"]
                         [:-7], my_review.updated_at.isoformat()[:-7])

    def test_to_dict_data_type(self):
        """Test to check if instance is json compatible"""

        my_review = Review()
        my_review.text = "Good"
        my_review.place_id = "12121"
        my_review.user_id = "10000"
        my_review_json = my_review.to_dict()

        self.assertIsInstance(my_review_json["text"], str)
        self.assertIsInstance(my_review_json["id"], str)
        self.assertIsInstance(my_review_json["place_id"], str)
        self.assertIsInstance(my_review_json["__class__"], str)
        self.assertIsInstance(my_review_json["created_at"], str)
        self.assertIsInstance(my_review_json["updated_at"], str)

    def test_review_kwargs_initialization(self):
        """Test for when kwargs is passed as review param"""

        my_review = Review()
        my_review.text = "Good"
        my_review.place_id = "12121"
        my_review.user_id = "10000"
        my_review_json = my_review.to_dict()
        my_new_review = Review(**my_review_json)

        self.assertNotEqual(my_new_review.created_at,
                            my_review_json["created_at"])
        self.assertNotEqual(my_new_review.updated_at,
                            my_review_json["updated_at"])
        self.assertEqual(my_new_review.text, my_review_json["text"])
        self.assertEqual(my_new_review.place_id, my_review_json["place_id"])
        self.assertEqual(my_new_review.id, my_review_json["id"])
        self.assertFalse(my_review is my_new_review)

    def test_new(self):
        """Test to check new() method behaviour"""
        obj = Review()
        self.storage.new(obj)
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.assertIn(key, self.storage.all())

    def test_save(self):
        """Test to check save() method behaviour"""
        obj = Review()
        self.storage.new(obj)
        self.storage.save()
        self.assertTrue(os.path.exists(self.file_path))
        key = f"{obj.__class__.__name__}.{obj.id}"
        with open(self.file_path) as f:
            data = json.load(f)
        self.assertIn(key, data)

    def test_reload(self):
        """Test to check reload() method behaviour"""
        obj = Review()
        self.storage.new(obj)
        self.storage.save()
        self.storage._FileStorage__objects = {}
        self.storage.reload()
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.assertIn(key, self.storage.all())

    def test_instance_deletion(self):
        """Test for behaviour after destroying an instance"""
        obj = Review()
        self.storage.new(obj)
        self.storage.save()
        obj_key = f"{obj.__class__.__name__}.{obj.id}"
        del obj
        self.storage.reload()
        self.storage._FileStorage__objects.clear()
        self.assertNotIn(obj_key, self.storage.all())

    def test_instance_diff(self):
        """Test inequality of two BaseModel Instance"""

        my_review = Review()
        my_review1 = Review()

        self.assertNotEqual(my_review, my_review1)


if __name__ == "__main__":
    unittest.main()
