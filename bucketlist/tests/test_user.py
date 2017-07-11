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


class InitialTests(unittest.TestCase):

    def register_user(self):
        """Registers new users to the system"""

        # new user Registration data
        new_user = {"fullnames": "Daisy Macharia",
                    "email": "test@example.org",
                    "password": "test_pass",
                    "confirm_password": "test_pass"}
        return self.client.post("/api/v1.0/auth/register", data=json.dumps
                                (new_user),
                                content_type="application/json")

    def login_user(self):
        return self.client.post("/api/v1.0/auth/login", data=json.dumps
                                ({"email": "test@example.org",
                                  "password": "test_pass"}),
                                content_type="application/json")

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.app_context = self.app.app_context()
        self.app_context.push()

        # create all tables
        db.create_all()

        # create a test client for our application
        self.client = self.app.test_client()

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    def test_register_user(self):
        res = self.register_user()
        self.assertIn('User added successfully', str(res.data))

    def test_register_existing_user(self):
        self.register_user()
        res1 = self.register_user()
        # self.assertEqual(res1.status, 409)
        self.assertIn('Email already in use', str(res1.data))

    def test_register_user_with_missing_email(self):
        test_blank = {"email": " ", "fullnames": "test blank",
                      "password": "test_pass"}
        res1 = self.client.post("/api/v1.0/auth/register", data=json.dumps(
                                test_blank), content_type="application/json")
        self.assertIn('Not a valid email address', str(res1.data))

    def test_login_user(self):
        self.register_user()
        res1 = self.login_user()
        self.assertIn('Login successful', str(res1.data))

    # def test_login_wrong_credentials(self):
    #     test_wrong_credentials = {"email": "test@example.org",
    #                               "password": "test_wrong"}
    #     self.register_user()
    #     res1 = self.client.post("/api/v1.0/auth/login", data=json.dumps(
    #                             test_wrong_credentials))
    #     self.assertIn('Wrong password', str(res1.data))

    def test_login_without_registering_user(self):
        res = self.login_user()
        self.assertIn('Email not registered',
                      str(res.data))


if __name__ == "__main__":
    unittest.main()
