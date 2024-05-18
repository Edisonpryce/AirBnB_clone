#!/user/bin/python
""" unittesting for the base model """

from models.base_model import BaseModel
import unittest
from uuid import uuid4
from datetime import datetime


class TestBaseModel(unittest.TestCase):
    """ unittests for base model defined """

    def setUp(self):
        """ proceeding tests setup"""
        self.model = BaseModel()
        self.model.name = "My First Model"
        self.model.my_number = 89

    def test_id_type(self):
        """ test for id """
        self.assertEqual(type(self.model.id), str)

    def test_created_at_type(self):
        """ test for created at """
        self.assertEqual(type(self.model.created_at), datetime)

    def test_updated_at_type(self):
        """ test for updated at """
        self.assertEqual(type(self.model.updated_at), datetime)

    def test_name_type(self):
        """ test for name type """
        self.assertEqual(type(self.model.name), str)


if __name__ == "__main__":
    unittest.main()
