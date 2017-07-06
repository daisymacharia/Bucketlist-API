import unittest
import json
from tests.setup import BaseTest


class InitialTests(BaseTest):

    def bucketlist(self):
        return self.client.post("/api/v1.0/bucketlists/", data=json.dumps
                                (self.new_bucketlist),
                                content_type="application/json")

    def test_create_bucketlists(self):
        """Test can create a bucketlist (POST request)"""
        res = self.bucketlist()
        self.assertEqual(res.status_code, 201)
        self.assertIn('Fly in the air', str(res.data))

    def test_create_existing_bucketlists(self):
        """Test cannot create a bucketlist that already exists"""
        self.bucketlist()
        res1 = self.bucketlist()
        self.assertEqual(res1.status_code, 409)

    def test_get_all_bucketlists(self):
        """Test can get all the bucketlists in the database"""
        self.bucketlist()
        result = self.client.get('/api/v1.0/bucketlists/')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Fly in the air', str(result.data))

    def test_get_bucketlists_by_id(self):
        """Test can get bucketlists using their id"""
        self.bucketlist()
        result = self.client.get('/api/v1.0/bucketlists/1')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Fly in the air', str(result.data))

    def test_get_bucketlists_that_dont_exist(self):
        """Test cannot get a non existent bucketlist"""
        result = self.client.get('/api/v1.0/bucketlists/9')
        self.assertEqual(result.status_code, 404)

    def test_update_bucketlists(self):
        """Test can update a bucketlists details"""
        self.bucketlist()
        result = self.client.put('/api/v1.0/bucketlists/1', data=json.dumps({
            "name": "Jump from a plane"}))
        self.assertEqual(result.status_code, 200)
        result = self.client.get('/bucketlists/v1.0/')
        self.assertIn("Jump from a plane", str(result.data))

    def test_update_non_existent_bucketlists(self):
        """Test cannot update a non existent bucketlist"""
        result = self.client.put('/api/v1.0/bucketlists/9', data=json.dumps({
            "name": "Jump from a plane"}))
        self.assertEqual(result.status_code, 404)
        self.assertIn("Bucketlist not found", str(result.data))

    def test_delete__bucketlists(self):
        """Test that a bucketlist can be deleted"""
        self.bucketlist()
        result = self.client.delete('/api/v1.0/bucketlists/1')
        self.assertEqual(result.status_code, 200)

    def test_delete_non_existent_bucketlists(self):
        """Test that a non exixtent bucketlist cannot be deleted"""
        result = self.client.delete('/api/v1.0/bucketlists/9')
        self.assertEqual(result.status_code, 404)


if __name__ == "__main__":
    unittest.main()
