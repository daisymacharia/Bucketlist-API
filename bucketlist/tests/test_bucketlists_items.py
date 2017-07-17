import unittest
import json
import os.path
import sys
from inspect import getsourcefile

current_path = os.path.abspath(getsourcefile(lambda: 0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

sys.path.insert(0, parent_dir)
from tests.setup import BaseTest
from app import create_app
from app.models import db


class InitialTests(BaseTest):

    def bucketlistitem(self):
        """
            Create a bucketlist item
        """
        self.client.post("/api/v1.0/bucketlists/",
                         data=json.dumps(self.new_bucketlist),
                         headers=self.headers)
        self.new_bucketlistitem = {'name': 'Test item'}
        return self.client.post("/api/v1.0/bucketlists/1/items/",
                                data=json.dumps(self.new_bucketlistitem),
                                headers=self.headers)

    def test_create_bucket_list_item(self):
        """Test that a bucketlist item is created successfully"""
        res = self.bucketlistitem()
        self.assertIn("Item Test item created successfully", str(res.data))
        self.assertEqual(res.status_code, 201)

    def test_create_existing_bucketlists_item(self):
        """Tests that items cannot be created with same name
           for same bucketlist"""
        self.bucketlistitem()
        result = self.bucketlistitem()
        self.assertIn("Item already created", str(result.data))
        self.assertEqual(result.status_code, 409)

    def test_create_items_with_empty_values(self):
        res = self.client.post("/api/v1.0/bucketlists/1/items/",
                               data=json.dumps({"name": " "}),
                               headers=self.headers)
        self.assertIn("Shorter than minimum length 3", str(res.data))

    def test_update_bucketlist_with_same_name(self):
        """Test cannot update a bucketlist with same data"""
        self.bucketlistitem()
        result = self.client.put('/api/v1.0/bucketlists/1/items/1',
                                 data=json.dumps({"name": "Test item"}),
                                 headers=self.headers)
        self.assertIn("Updating with same data not allowed", str(result.data))
        self.assertEqual(result.status_code, 409)

    def test_update_bucketlists_item(self):
        self.bucketlistitem()
        second_bucketlist = {"name": "sky diving"}
        result = self.client.put("/api/v1.0/bucketlists/1/items/1",
                                 data=json.dumps(second_bucketlist),
                                 headers=self.headers)
        self.assertEqual(result.status_code, 200)

    def get_bucketlists_items_by_id(self):
        self.bucketlistitem()
        result = self.client.get("/api/v1.0/bucketlists/1/items/1")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Test item", str(result.data))

    def get_bucketlists_items(self):
        self.bucketlistitem()
        result = self.client.get("/api/v1.0/bucketlists/1/items/",
                                 headers=self.headers)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Test item", str(result.data))

    def test_search_bucketlist_items_using_name(self):
        self.bucketlistitem()
        result = self.client.get('/api/v1.0/bucketlists/1/items/?q=item',
                                 headers=self.headers)
        self.assertIn('Test item', str(result.data))
        self.assertEqual(result.status_code, 200)

    def test_pagination(self):
        self.bucketlistitem()
        result = self.client.get('/api/v1.0/bucketlists/1/items/?limit=1',
                                 headers=self.headers)
        self.assertIn('"total_pages": 1', str(result.data))
        self.assertEqual(result.status_code, 200)

    def get_non_existent_bucketlists_items(self):
        result = self.client.get("/api/v1.0/bucketlists/1/items/9",
                                 headers=self.headers)
        self.assertIn('The bucketlist item does not exist', str(result.data))
        self.assertEqual(result.status_code, 404)

    def test_delete_bucketlists_items(self):
        self.bucketlistitem()
        result = self.client.delete("/api/v1.0/bucketlists/1/items/1",
                                    headers=self.headers)
        self.assertIn("Successfully deleted bucketlist item Test item",
                      str(result.data))
        self.assertEqual(result.status_code, 200)

    def test_delete_bucketlists_items_from_non_existent_bucketlist(self):
        self.bucketlistitem()
        result = self.client.delete("/api/v1.0/bucketlists/2/items/1",
                                    headers=self.headers)
        self.assertIn("Bucketlist not found", str(result.data))
        self.assertEqual(result.status_code, 404)

    def test_delete_non_existent_bucketlists_items(self):
        self.bucketlistitem()
        result = self.client.delete("/api/v1.0/bucketlists/1/items/9",
                                    headers=self.headers)
        self.assertIn("The bucketlist item does not exist", str(result.data))
        self.assertEqual(result.status_code, 404)


if __name__ == "__main__":
    unittest.main()
