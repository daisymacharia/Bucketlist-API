import unittest
import os
import json
from unittest import TestCase
from flask import json

from tests.setup import BaseTest

class InitialTests(BaseTest):

    def bucketlist(self):
        """
            Create a bucketlist
        """
        bucketlist = {"name": "Travel"}
        self.client.post("/bucketlists/",
                         data=json.dumps({"name": "Test Item"}),
                         headers=self.headers)

    def test_create_bucket_lists(self):
        pass
    def test_create_existing_bucket_lists(self):
        pass
    def test_create_new_item_in_bucket_lists(self):
        pass
    def test_get_all_bucket_lists(self):
        pass
    def test_get_bucket_lists_by_id(self):
        pass
    def test_get_non_existent_bucket_lists(self):
        pass
    def test_update_bucket_lists(self):
        pass
    def test_update_non_existent_bucket_lists(self):
        pass
    def test_read_bucket_lists(self):
        pass
    def test_read_non_existent_bucketlists(self):
        pass
    def test_delete__bucket_lists(self):
        pass
    def test_delete_item_in_bucket_lists(self):
        pass
    def test_delete_non_existent_bucketlists(self):
        pass

if __name__ == "__main__":
    unittest.main()
