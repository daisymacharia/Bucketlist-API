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


class BucketListItemsTests(unittest.TestCase):
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
                         (self.new_user),
                         content_type="application/json")

        # login user
        response = self.client.post("/api/v1.0/auth/login", data=json.dumps
                                    ({"email": "test@example.org",
                                      "password_hash": "test_pass"}),
                                    content_type="application/json")
        self.new_bucketlist = {'name': 'Go bunjee jumping'}
        self.client.post("/api/v1.0/bucketlists/", data=json.dumps
                         (self.new_bucketlist),
                         content_type="application/json")

        self.new_bucketlistitem = {'name': 'Test item'}

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    def bucketlistitem(self):
        """
            Create a bucketlist item
        """

        return self.client.post("/api/v1.0/bucketlists/1/items",
                                data=self.new_bucketlistitem)

    def test_create_bucket_list_item(self):
        res = self.bucketlistitem()
        self.assertEqual(res.status_code, 201)
        self.assertIn('Test item', str(res.data))

    def test_create_existing_bucketlists_item(self):
        self.bucketlistitem()
        result = self.bucketlistitem()
        self.assertEqual(result.status_code, 409)

    def test_create_items_with_empty_values(self):
        res = self.client.post("/api/v1.0/bucketlists/1/items",
                               data=json.dumps({"name": " "}))
        self.assertEqual(res.status_code, 400)

    def test_update_bucketlists_item(self):
        self.bucketlistitem()
        second_bucketlist = {"name": "sky diving"}
        result = self.client.put("/api/v1.0/bucketlists/1/items/1",
                                 data=json.dumps(second_bucketlist))
        self.assertEqual(result.status_code, 200)

    def get_bucketlists_items_by_id(self):
        self.bucketlistitem()
        result = self.client.get("/api/v1.0/bucketlists/1/items/1")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Test item", str(result.data))

    def get_bucketlists_items(self):
        self.bucketlistitem()
        result = self.client.get("/api/v1.0/bucketlists/1/items")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Test item", str(result.data))

    def get_non_existent_bucketlists_items(self):
        result = self.client.get("/api/v1.0/bucketlists/1/items/9")
        self.assertEqual(result.status_code, 404)

    def test_delete_bucketlists_items(self):
        self.bucketlistitem()
        result = self.client.delete("/api/v1.0/bucketlists/1/items/1")
        self.assertEqual(result.status_code, 200)

    def test_delete_non_existent_bucketlists_items(self):
        result = self.client.delete("/api/v1.0/bucketlists/1/items/9")
        self.assertEqual(result.status_code, 404)


if __name__ == "__main__":
    unittest.main()
