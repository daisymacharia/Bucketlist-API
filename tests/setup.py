import unittest
import os
import json
from app import app


class BaseTest(unittest.TestCase):
    """ Initialising TestCase"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = config_name="testing"
        self.bucketlist = {'name': 'Bunjee jumping'}

        # create all tables
        # db.create_all()

    def tearDown(self):
        """teardown all initialized variables."""
            # drop all tables
        # db.session.remove()
        # db.drop_all()

if __name__ == "__main__":
    unittest.main()
