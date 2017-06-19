import unittest
import json
from setup import BaseTest


class InitialTests(BaseTest):

    def bucketlistitem(self):
        """
            Create a bucketlist item
        """
        return self.client.post("/api/v1.0/bucketlists/items/",
                                data=self.new_bucketlistitem)

    def test_create_bucket_list_item(self):
        res = self.bucketlistitem()
        self.assertEqual(res.status_code, 201)
        self.assertIn('Test item', str(res.data))

    def test_create_existing_bucketlists_item(self):
        res = self.bucketlistitem()
        self.assertEqual(res.status_code, 201)
        result = self.bucketlistitem()
        self.assertEqual(result.status_code, 400)

    def test_create_items_with_empty_values(self):
        res = self.client.post("/api/v1.0/bucketlists/items/",
                               data=json.dumps({"name": " "}))
        self.assertEqual(res.status_code, 400)

    def test_update_bucketlists_item(self):
        res = self.bucketlistitem()
        self.assertEqual(res.status_code, 201)
        second_bucketlist = {"name": "sky diving"}
        result = self.client.put("/api/v1.0/bucketlists/items/",
                                 data=json.dumps(second_bucketlist))
        self.assertEqual(result.status_code, 200)
        result2 = self.client.get('/api/v1.0/bucketlists/items/')
        self.assertIn("Go sky diving", str(result2.data))

    def get_bucketlists_items_by_id(self):
        res = self.bucketlistitem()
        self.assertEqual(res.status_code, 201)
        result = self.client.get("/api/v1.0/bucketlists/items/1")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Test item", str(result.data))

    def get_bucketlists_items(self):
        res = self.bucketlistitem()
        self.assertEqual(res.status_code, 201)
        result = self.client.get("/api/v1.0/bucketlists/items/")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Test item", str(result.data))

    def get_non_existent_bucketlists_items(self):
        result = self.client.get("/api/v1.0/bucketlists/items/9")
        self.assertEqual(result.status_code, 404)

    def test_delete_bucketlists_items(self):
        res = self.bucketlistitem()
        self.assertEqual(res.status_code, 201)
        result = self.client.delete("/api/v1.0/bucketlists/items/1")
        self.assertEqual(result.status_code, 200)
        result1 = self.client.get("/api/v1.0/bucketlists/items/1")
        self.assertEqual(result1.status_code, 404)

    def test_delete_non_existent_bucketlists_items(self):
        result = self.client.delete("/api/v1.0/bucketlists/items/9")
        self.assertEqual(result.status_code, 400)


if __name__ == "__main__":
    unittest.main()
