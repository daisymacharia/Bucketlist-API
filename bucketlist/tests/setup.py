import unittest
import json
import os.path
import sys
from inspect import getsourcefile

current_path = os.path.abspath(getsourcefile(lambda: 0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

sys.path.insert(0, parent_dir)
from app import create_app
from app.models import db


class BaseTest(unittest.TestCase):
    """ Initialising TestCase"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.app_context = self.app.app_context()
        self.app_context.push()

        # create all tables
        db.create_all()

        # create a test client for our application
        self.client = self.app.test_client()

        # new user Registration data
        self.new_user = {"fullnames": "Daisy Macharia",
                         "email": "test@example.org",
                         "password_hash": "test_pass",
                         "confirm_password": "test_pass"}

        # Register user
        self.client.post("/api/v1.0/auth/register", data=json.dumps
                         (self.new_user), content_type="application/json")

        # login user
        response = self.client.post("/api/v1.0/auth/login", data=json.dumps
                                    ({"email": "test@example.org",
                                      "password_hash": "test_pass"}),
                                    content_type="application/json")

        self.new_bucketlist = {'name': 'Go bunjee jumping'}
        self.new_bucketlistitem = {'name': 'Go bunjee jumping'}

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
