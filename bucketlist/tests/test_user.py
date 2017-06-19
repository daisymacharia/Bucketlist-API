import unittest
import json
from setup import BaseTest


class InitialTests(BaseTest):

    def register_user(self):
        return self.client.post("/api/v1.0/auth/register", data=json.dumps
                                (self.new_user),
                                content_type="application/json")

    def login_user(self):
        return self.client.post("/api/v1.0/auth/login", data=json.dumps
                                ({"username": "test_name",
                                 "password_hash": "test_pass"}),
                                content_type="application/json")

    def test_register_user(self):
        res = self.register_user()
        self.assertEqual(res.status_code, 201)
        self.assertIn('Registration successful', str(res.data))

    def test_register_existing_user(self):
        res = self.register_user()
        self.assertEqual(res.status_code, 201)
        res1 = self.register_user()
        self.assertEqual(res1.status_code, 400)
        self.assertIn('User already exists', str(res1.data))

    def test_register_user_with_missing_email(self):
        test_blank = {"email": " ", "username": "test_blank",
                      "password_hash": "test_pass"}
        res1 = self.client.post("/api/v1.0/auth/register", data=json.dumps(
                                test_blank), content_type="application/json")
        self.assertEqual(res1.status_code, 400)
        self.assertIn('Email cannot be blank', str(res1.data))

    def test_login_user(self):
        res = self.register_user()
        self.assertEqual(res.status_code, 201)
        res1 = self.login_user()
        self.assertEqual(res1.status_code, 200)
        self.assertIn('Login successful', str(res1.data))

    def test_login_wrong_credentials(self):
        test_wrong_credentials = {"username": "test_name",
                                  "password_hash": "test_wrong"}
        res = self.register_user()
        self.assertEqual(res.status_code, 201)
        res1 = self.client.post("/api/v1.0/auth/login", data=json.dumps(
                                test_wrong_credentials))
        self.assertEqual(res1.status_code, 401)
        self.assertIn('Wrong login password', str(res1.data))

    def test_login_without_registering_user(self):
        res = self.login_user()
        self.assertEqual(res.status_code, 400)
        self.assertIn('You are required to first register a new user',
                      str(res.data))

    def test
