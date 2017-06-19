import unittest
import os.path
import sys
from inspect import getsourcefile

current_path = os.path.abspath(getsourcefile(lambda: 0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

sys.path.insert(0, parent_dir)
from app import create_app, db


class BaseTest(unittest.TestCase):
    """ Initialising TestCase"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app("testing")
        self.database = db
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        # create all tables
        self.database.drop_all()
        self.database.create_all()
        self.new_bucketlist = {'name': 'Go bunjee jumping'}
        self.new_bucketlistitem = {'name': 'Test item'}
        self.user = {"email": "test@example.org", "password_hash": "test_pass"}

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
