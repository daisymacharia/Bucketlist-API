import unittest
import json
from setup import BaseTest


class InitialTests(BaseTest):

    def bucketlist(self):
        return self.client.post("/api/v1.0/bucketlists/", data=json.dumps
                                (self.new_bucketlist))

    def test_create_bucketlists(self):
        """Test API can create a bucketlist (POST request)"""
        res = self.bucketlist()
        self.assertEqual(res.status_code, 201)
        self.assertIn('Go bunjee jumping', str(res.data))

    def test_create_existing_bucketlists(self):
        """Test API cannot create a bucketlist that already exists"""
        res = self.bucketlist()
        self.assertEqual(res.status_code, 201)
        res1 = self.bucketlist()
        self.assertEqual(res1.status_code, 400)

    def test_get_all_bucketlists(self):
        """Test API can get all the bucketlists in the database"""
        res = self.bucketlist()
        self.assertEqual(res.status_code, 201)
        result = self.client.get('/api/v1.0/bucketlists/')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Go bunjee jumping', str(result.data))

    def test_get_bucketlists_item_by_id(self):
        """Test API can get bucketlists using their id"""
        res = self.bucketlist()
        self.assertEqual(res.status_code, 201)
        result = self.client.get('/api/v1.0/bucketlists/1')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Go bunjee jumping', str(result.data))

    def test_get_non_existent_bucketlists(self):
        result = self.client.get('/api/v1.0/bucketlists/9/')
        self.assertEqual(result.status_code, 404)

    def test_update_bucketlists(self):
        res = self.bucketlist()
        self.assertEqual(res.status_code, 201)
        result = self.client.put('/api/v1.0/bucketlists/1', data=json.dumps({
                "name": "Go sky diving"}))
        self.assertEqual(result.status_code, 200)
        result = self.client.get('/bucketlists/v1.0/')
        self.assertIn("Go sky diving", str(result.data))

    def test_update_non_existent_bucketlists(self):
        result = self.client.put('/api/v1.0/bucketlists/9', data=json.dumps({
                "name": "Go sky diving"}))
        self.assertEqual(result.status_code, 400)

    def test_delete__bucketlists(self):
        res = self.bucketlist()
        self.assertEqual(res.status_code, 201)
        result = self.client.delete('/api/v1.0/bucketlists/1')
        self.assertEqual(result.status_code, 200)
        result = self.client.get('/bucketlists/v1.0/1')
        self.assertEqual(result.status_code, 404)

    def test_delete_non_existent_bucketlists(self):
        result = self.client.delete('/api/v1.0/bucketlists/9')
        self.assertEqual(result.status_code, 400)


if __name__ == "__main__":
    unittest.main()
