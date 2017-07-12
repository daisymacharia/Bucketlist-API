import unittest
import json
from tests.setup import BaseTest


class InitialTests(BaseTest):

    def bucketlist(self):
        return self.client.post("/api/v1.0/bucketlists/",
                                data=json.dumps(self.new_bucketlist),
                                headers=self.headers)

    def test_create_bucketlists(self):
        """Test can create a bucketlist (POST request)"""
        res = self.bucketlist()
        self.assertIn("Bucketlist 1 created successfully",
                      str(res.data))

    def test_create_existing_bucketlists(self):
        """Test cannot create a bucketlist that already exists"""
        self.bucketlist()
        res1 = self.bucketlist()
        self.assertIn("Bucketlist already created",
                      str(res1.data))

    def test_create_bucketlist_with_empty_values(self):
        res = self.client.post("/api/v1.0/bucketlists/",
                               data=json.dumps({"name": " "}),
                               headers=self.headers)
        self.assertIn("Shorter than minimum length 3", str(res.data))

    def test_get_all_bucketlists(self):
        """Test can get all the bucketlists in the database"""
        self.bucketlist()
        result = self.client.get('/api/v1.0/bucketlists/',
                                 headers=self.headers)
        self.assertIn('Go bunjee jumping', str(result.data))

    def test_get_bucketlists_by_id(self):
        """Test can get bucketlists using their id"""
        self.bucketlist()
        result = self.client.get('/api/v1.0/bucketlists/1/',
                                 headers=self.headers)
        self.assertIn('Go bunjee jumping', str(result.data))

    def test_get_bucketlists_that_dont_exist(self):
        """Test cannot get a non existent bucketlist"""
        self.bucketlist()
        result = self.client.get('/api/v1.0/bucketlists/9/',
                                 headers=self.headers)
        self.assertIn('The bucketlist does not exist', str(result.data))

    def test_update_bucketlists(self):
        """Test can update a bucketlists details"""
        self.bucketlist()
        result = self.client.put('/api/v1.0/bucketlists/1/',
                                 data=json.dumps({"name": "Jump from a plane"}),
                                 headers=self.headers)
        self.assertEqual(result.status_code, 200)
        result = self.client.get('/api/v1.0/bucketlists/1/',
                                 headers=self.headers)
        self.assertIn("Jump from a plane", str(result.data))

    def test_update_non_existent_bucketlists(self):
        """Test cannot update a non existent bucketlist"""
        self.bucketlist()
        result = self.client.put('/api/v1.0/bucketlists/9/',
                                 data=json.dumps({"name": "Jump from a plane"}),
                                 headers=self.headers)
        self.assertIn("The bucketlist does not exist", str(result.data))

    def test_update_bucketlist_with_same_name(self):
        """Test cannot update a bucketlist with same data"""
        self.bucketlist()
        result = self.client.put('/api/v1.0/bucketlists/1/',
                                 data=json.dumps({"name": "Go bunjee jumping"}),
                                 headers=self.headers)
        self.assertIn("Updating with same data not allowed", str(result.data))

    def test_delete__bucketlists(self):
        """Test that a bucketlist can be deleted"""
        self.bucketlist()
        result = self.client.delete('/api/v1.0/bucketlists/1/',
                                    headers=self.headers)
        self.assertEqual(result.status_code, 200)

    def test_delete_non_existent_bucketlists(self):
        """Test that a non exixtent bucketlist cannot be deleted"""
        self.bucketlist()
        result = self.client.delete('/api/v1.0/bucketlists/9/',
                                    headers=self.headers)
        self.assertIn('The bucketlist does not exist', str(result.data))


if __name__ == "__main__":
    unittest.main()
