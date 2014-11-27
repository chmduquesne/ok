import ok
import os
import unittest

# Available methods on responses objects: see
# http://werkzeug.pocoo.org/docs/0.9/quickstart/#responses

class OkTestCase(unittest.TestCase):

    def setUp(self):
        ok.app.config["TESTING"] = True
        self.app = ok.app.test_client()

    def tearDown(self):
        pass

    def test_root_status(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_ok_status(self):
        response = self.app.get("/ok/")
        self.assertEqual(response.status_code, 400)

    def test_users_status(self):
        response = self.app.get("/users/")
        self.assertEqual(response.status_code, 200)

    def test_groups_status(self):
        response = self.app.get("/groups/")
        self.assertEqual(response.status_code, 200)

    def test_restrictions_status(self):
        response = self.app.get("/restrictions/")
        self.assertEqual(response.status_code, 200)
