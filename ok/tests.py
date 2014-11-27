import ok
import os
import unittest
import json

# Available methods on responses objects: see
# http://werkzeug.pocoo.org/docs/0.9/quickstart/#responses

class OkStatusTestCase(unittest.TestCase):

    def setUp(self):
        ok.app.config["TESTING"] = True
        self.app = ok.app.test_client()

    def tearDown(self):
        pass

    def test_root_status(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_ok_no_arg(self):
        response = self.app.get("/ok/")
        body = json.loads(response.data)
        self.assertEqual(body["message"], "Expected a url argument")
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

    def test_post_put_get_delete_user(self):
        # create user john, part of group_1 and group_2
        response = self.app.post("/users/john",data={"groups":
            "group_1,group_2"})
        self.assertEqual(response.status_code, 200)
        # check that john exists and is part of group_1 and group_2
        response = self.app.get("/users/john")
        groups = json.loads(response.data)
        self.assertIn("group_1", groups["groups"])
        self.assertIn("group_2", groups["groups"])
        self.assertIn("users", groups["groups"])
        # modify john to be part of group_3 and group_4 instead
        response = self.app.put("/users/john", data={"groups":
            "group_3,group_4"})
        self.assertEqual(response.status_code, 200)
        # check that john exists and now part of group_3 and group_4, and
        # that he is not in group_1 and group_2 any more
        response = self.app.get("/users/john")
        groups = json.loads(response.data)
        self.assertNotIn("group_1", groups["groups"])
        self.assertNotIn("group_2", groups["groups"])
        self.assertIn("group_3", groups["groups"])
        self.assertIn("group_4", groups["groups"])
        # delete john
        response = self.app.delete("/users/john")
        self.assertEqual(response.status_code, 204)
        # check that john now returns a 404 error
        response = self.app.get("/users/john")
        self.assertEqual(response.status_code, 404)

    def test_ok(self):
        response = self.app.get("/ok/?url=%2F&groups=admin")
        self.assertEqual(response.status_code, 200)
