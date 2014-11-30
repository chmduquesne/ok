from __future__ import with_statement
import ok
import os
import unittest
import json
import tempfile
import shutil

# Available methods on responses objects: see
# http://werkzeug.pocoo.org/docs/0.9/quickstart/#responses

CONFIG_RESET ="""
TESTING=True
CONFIG=%s
USERS_DB="%s/users.kch"
GROUPS_DB="%s/groups.json"
AUTO_CREATE=True
DEFAULT_GROUPS=["users"]
"""

CONFIG_RESTRICTIONS="""
from ok.restrictions import restrictions_manager

@restrictions_manager.register()
def myrestriction(*args, **kwargs):
    \"\"\"
    This restriction allows nothing
    \"\"\"
    return False
"""

class OkAppTestCase(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.reset_config()
        self.app = ok.app.test_client()

    def tearDown(self):
        self.reset_config()
        shutil.rmtree(self.tempdir)

    def reset_config(self):
        ok.app.config.update(dict(
            TESTING=True,
            CONFIG=os.path.join(self.tempdir, "config.py"),
            USERS_DB=os.path.join(self.tempdir, "users.kch"),
            GROUPS_DB=os.path.join(self.tempdir, "groups.json"),
            AUTO_CREATE=True,
            DEFAULT_GROUPS=["users"]
            ))

    def test_import_config(self):
        with open(ok.app.config["CONFIG"], "wb") as f:
            f.write("AUTO_CREATE=False")
        ok.app.config.from_pyfile(ok.app.config["CONFIG"])
        self.assertEqual(ok.app.config["AUTO_CREATE"], False)

    def test_import_restriction(self):
        response = self.app.get("/restrictions/")
        restriction_list = json.loads(response.data)
        self.assertNotIn("myrestriction", restriction_list)
        with open(ok.app.config["CONFIG"], "wb") as f:
            f.write(CONFIG_RESTRICTIONS)
        ok.app.config.from_pyfile(ok.app.config["CONFIG"])
        response = self.app.get("/restrictions/")
        restriction_list = json.loads(response.data)
        self.assertIn("myrestriction", restriction_list)

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


class DictionaryTestCase():

    def setUp(self):
        raise NotImplementedError

    def tearDown(self):
        raise NotImplementedError

    def get_dictionary(self):
        raise NotImplementedError

    def assertInSyncWithCopy(self, dictionary):
        raise NotImplementedError

    def test_empty(self):
        d = self.get_dictionary()
        self.assertInSyncWithCopy(d)

    def test_len(self):
        d = self.get_dictionary()
        self.assertEqual(len(d), 0)
        for key in ["a", "b", "c"]:
            d[key] = key
        self.assertEqual(len(d), 3)
        self.assertInSyncWithCopy(d)

    def test_getitem_empty(self):
        d = self.get_dictionary()
        with self.assertRaises(KeyError):
            d["does not exist"]
        self.assertInSyncWithCopy(d)

    def test_getitem_assign(self):
        d = self.get_dictionary()
        for key in ["a", "b", "c"]:
            d[key] = key
        self.assertEqual(d["a"], "a")
        self.assertEqual(d["b"], "b")
        self.assertEqual(d["c"], "c")
        self.assertInSyncWithCopy(d)

    def test_delete_empty(self):
        d = self.get_dictionary()
        with self.assertRaises(KeyError):
            del d["does not exist"]
        self.assertInSyncWithCopy(d)

    def test_delete(self):
        d = self.get_dictionary()
        d["a"] = "a"
        self.assertEqual(d["a"], "a")
        del d["a"]
        with self.assertRaises(KeyError):
            del d["a"]
        self.assertInSyncWithCopy(d)

    def test_in(self):
        d = self.get_dictionary()
        self.assertEqual("a" in d, False)
        d["a"] = "a"
        self.assertEqual("a" in d, True)
        self.assertInSyncWithCopy(d)

    def test_not_in(self):
        d = self.get_dictionary()
        self.assertEqual("a" not in d, True)
        d["a"] = "a"
        self.assertEqual("a" not in d, False)
        self.assertInSyncWithCopy(d)

    def test_iter(self):
        d = self.get_dictionary()
        for key in ["a", "b", "c"]:
            d[key] = key
        for key in iter(d):
            self.assertEqual(d[key], key)
        self.assertInSyncWithCopy(d)

    def test_iter_for_in(self):
        d = self.get_dictionary()
        for key in ["a", "b", "c"]:
            d[key] = key
        for key in d:
            self.assertEqual(d[key], key)
        self.assertInSyncWithCopy(d)

    def test_clear(self):
        d = self.get_dictionary()
        for key in ["a", "b", "c"]:
            d[key] = key
        self.assertEqual(len(d), 3)
        d.clear()
        self.assertEqual(len(d), 0)
        self.assertInSyncWithCopy(d)

    def test_get_empty(self):
        d = self.get_dictionary()
        res = d.get("does not exist")
        self.assertEqual(res, None)
        self.assertInSyncWithCopy(d)

    def test_get_default(self):
        d = self.get_dictionary()
        res = d.get("does not exist", "default value")
        self.assertEqual(res, "default value")
        self.assertInSyncWithCopy(d)

    def test_get(self):
        d = self.get_dictionary()
        for key in ["a", "b", "c"]:
            d[key] = key
        for key in d:
            self.assertEqual(d.get(key), key)
        self.assertInSyncWithCopy(d)

    def test_has_key(self):
        d = self.get_dictionary()
        self.assertEqual(d.has_key("a"), False)
        d["a"] = "a"
        self.assertEqual(d.has_key("a"), True)
        self.assertInSyncWithCopy(d)

    def test_items(self):
        d = self.get_dictionary()
        for key in ["a", "b", "c"]:
            d[key] = key
        for key, value in d.items():
            self.assertEqual(key, value)
        self.assertInSyncWithCopy(d)

    def test_iteritems(self):
        d = self.get_dictionary()
        for key in ["a", "b", "c"]:
            d[key] = key
        for key, value in d.iteritems():
            self.assertEqual(key, value)
        self.assertInSyncWithCopy(d)

    def test_iterkeys(self):
        d = self.get_dictionary()
        for key in ["a", "b", "c"]:
            d[key] = key
        for key in d.iterkeys():
            self.assertEqual(d[key], key)
        self.assertInSyncWithCopy(d)

    def test_itervalues(self):
        d = self.get_dictionary()
        for key in ["a", "b", "c"]:
            d[key] = key
        for value in d.itervalues():
            self.assertEqual(d[value], value)
        self.assertInSyncWithCopy(d)

    def test_keys(self):
        d = self.get_dictionary()
        for key in ["a", "b", "c"]:
            d[key] = key
        for key in d.keys():
            self.assertEqual(d[key], key)
        self.assertInSyncWithCopy(d)

    def test_pop_empty(self):
        d = self.get_dictionary()
        with self.assertRaises(KeyError):
            res = d.pop("does not exist")
        self.assertInSyncWithCopy(d)

    def test_pop_default(self):
        d = self.get_dictionary()
        res = d.pop("does not exist", "default value")
        self.assertEqual(res, "default value")
        self.assertInSyncWithCopy(d)

    def test_pop(self):
        d = self.get_dictionary()
        d["a"] = "a"
        res = d.pop("a")
        self.assertEqual(res, "a")
        self.assertInSyncWithCopy(d)

    def test_values(self):
        d = self.get_dictionary()
        for key in ["a", "b", "c"]:
            d[key] = key
        for value in d.values():
            self.assertEqual(d[value], value)
        self.assertInSyncWithCopy(d)

class JsonDictTestCase(DictionaryTestCase, unittest.TestCase):

    def setUp(self):
        fd, name = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        os.unlink(name)
        self.dict_path = name
        self.dictionary = ok.serializeddicts.JsonDict(self.dict_path)

    def get_dictionary(self):
        return self.dictionary

    def tearDown(self):
        os.unlink(self.dict_path)

    def assertInSyncWithCopy(self, dictionary):
        assert dictionary == ok.serializeddicts.JsonDict(self.dict_path)

class KyotoCabinetDictTestCase(DictionaryTestCase, unittest.TestCase):

    def setUp(self):
        fd, name = tempfile.mkstemp(suffix='.kch')
        os.close(fd)
        os.unlink(name)
        self.dict_path = name
        self.dictionary = ok.serializeddicts.KyotoCabinetDict(self.dict_path)

    def get_dictionary(self):
        return self.dictionary

    def tearDown(self):
        os.unlink(self.dict_path)

    def assertInSyncWithCopy(self, dictionary):
        assert dictionary == ok.serializeddicts.KyotoCabinetDict(self.dict_path)

