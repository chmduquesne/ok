# -*- coding: utf-8 -*-
from __future__ import with_statement
import ok
import os
import unittest
import json
import tempfile
import shutil
import urllib2

##
# Tests configurations
##

CUSTOM_RESTRICTION="""
from ok.restrictions import restrictions_manager

@restrictions_manager.register()
def myrestriction(*args, **kwargs):
    \"\"\"
    This restriction allows nothing
    \"\"\"
    return False
"""

CUSTOMIZED_DEFAULT_GROUPS="""
DEFAULT_GROUPS=["default", "all"]
"""

NO_AUTO_CREATE="""
AUTO_CREATE=False
"""

REDEFINES_RESTRICTION="""
from ok.restrictions import restrictions_manager

@restrictions_manager.register()
def unrestricted(*args, **kwargs):
    return False
"""

ADVANCED_RESTRICTIONS="""
from ok.restrictions import restrictions_manager

categories = {
    "fruits": ["banana", "apple"],
    "vegetables": ["eggplant"]
    }

@restrictions_manager.register(takes_extra_param=True)
def restricted_ingredient(groupname, http_scheme, http_netloc, http_path,
        http_query, http_fragment, http_username, http_password,
        http_hostname, http_port, http_method, http_data,
        restriction_params):
    \"\"\"
    Restrict the ingredient argument to a given category
    \"\"\"

    category = restriction_params

    if "ingredient" in http_query:
        return http_query["ingredient"] in categories[category]

    return True
"""

ADVANCED_RESTRICTIONS_CUSTOM_HINT="""
from ok.restrictions import restrictions_manager

def describer(description):
    return dict(((key, True) for key in description))

DESCRIBER=describer

categories = {
    "fruits": ["banana", "apple"],
    "vegetables": ["eggplant"]
    }

@restrictions_manager.register(takes_extra_param=True)
def restricted_ingredient(groupname, http_scheme, http_netloc, http_path,
        http_query, http_fragment, http_username, http_password,
        http_hostname, http_port, http_method, http_data,
        restriction_params):
    \"\"\"
    Restrict the ingredient argument to a given category
    \"\"\"

    category = restriction_params

    if "ingredient" in http_query:
        return http_query["ingredient"] in categories[category]

    return True
"""

##
# Helpers
##

def urlencode(s):
    return urllib2.quote(s.encode("utf-8"))

class OkConfig:
    """
    Helper class to load a configuration temporarily.

    Usage:
        >>> with OkConfig(sometext):
        >>>     do_stuff()
    """
    def __init__(self, config_text):
        self.config_file = self.mktemp()
        with open(self.config_file, "wb") as f:
            f.write(config_text)

    def mktemp(self):
        fd, filename = tempfile.mkstemp(suffix=".py")
        os.close(fd)
        return filename

    def save_app_config(self):
        self.saved_config = dict(
                TESTING=ok.app.config["TESTING"],
                USERS_DB=ok.app.config["USERS_DB"],
                GROUPS_DB=ok.app.config["GROUPS_DB"],
                AUTO_CREATE=ok.app.config["AUTO_CREATE"],
                DEFAULT_GROUPS=ok.app.config["DEFAULT_GROUPS"],
                DESCRIBER=ok.app.config["DESCRIBER"]
                )
        self.saved_restrictions = \
                ok.restrictions.restrictions_manager.func_map.keys()

    def restore_app_config(self):
        ok.app.config.update(self.saved_config)
        for restriction in \
                ok.restrictions.restrictions_manager.func_map.keys():
            if restriction not in self.saved_restrictions:
                ok.restrictions.restrictions_manager.forget(restriction)

    def load_text_config(self):
        os.environ["OK_CONFIG"] = self.config_file
        ok.api.load_config_from_envvar("OK_CONFIG")

    def __enter__(self):
        self.save_app_config()
        self.load_text_config()

    def __exit__(self, type, value, traceback):
        self.restore_app_config()
        os.unlink(self.config_file)

##
# Test cases
##

class OkAppTestCase(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        ok.app.config.update(dict(
            TESTING=True,
            USERS_DB=os.path.join(self.tempdir, "users.kch"),
            GROUPS_DB=os.path.join(self.tempdir, "groups.json"),
            ))
        self.app = ok.app.test_client()

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_import_config(self):
        with OkConfig("AUTO_CREATE=False"):
            self.assertEqual(ok.app.config["AUTO_CREATE"], False)
        self.assertEqual(ok.app.config["AUTO_CREATE"], True)

    def test_import_non_existing_config(self):
        ok.api.load_config_from_envvar("IDONTEXIST")
        with self.assertRaises(RuntimeError):
            ok.api.load_config_from_envvar("IDONTEXIST", silent=False)

    def test_load_unexisting_config(self):
        os.environ["OK_CONFIG"] = "/idontexist"
        config = dict(
                TESTING=ok.app.config["TESTING"],
                USERS_DB=ok.app.config["USERS_DB"],
                GROUPS_DB=ok.app.config["GROUPS_DB"],
                AUTO_CREATE=ok.app.config["AUTO_CREATE"],
                DEFAULT_GROUPS=ok.app.config["DEFAULT_GROUPS"]
                )
        ok.api.load_config_from_envvar("OK_CONFIG")
        self.assertEqual(dict( TESTING=ok.app.config["TESTING"],
            USERS_DB=ok.app.config["USERS_DB"],
            GROUPS_DB=ok.app.config["GROUPS_DB"],
            AUTO_CREATE=ok.app.config["AUTO_CREATE"],
            DEFAULT_GROUPS=ok.app.config["DEFAULT_GROUPS"]), config)

    def test_forget_restriction(self):
        with OkConfig(CUSTOM_RESTRICTION):
            rule = ok.restrictions.restrictions_manager.get("myrestriction")
            ok.restrictions.restrictions_manager.forget("myrestriction")
            with self.assertRaises(KeyError):
                rule = ok.restrictions.restrictions_manager.get("myrestriction")

    def test_import_restriction(self):
        response = self.app.get("/restrictions/")
        body = json.loads(response.data)
        self.assertNotIn("myrestriction", body)
        with OkConfig(CUSTOM_RESTRICTION):
            response = self.app.get("/restrictions/")
            body = json.loads(response.data)
            self.assertIn("myrestriction", body["restrictions"])

    def test_import_redefined_restriction(self):
        with self.assertRaises(KeyError):
            with OkConfig(REDEFINES_RESTRICTION):
                pass

    def test_config_url(self):
        response = self.app.get("/config/")
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.data)
        self.assertIn("USERS_DB", body)
        self.assertIn("GROUPS_DB", body)

    def test_users_url(self):
        response = self.app.get("/users/")
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body,
                {u'total_pages': 1, u'more_results': False, u'page': 1,
                    u'users': {}})

    def test_users_url_unexisting(self):
        response = self.app.get("/users/john")
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 404)

    def test_users_url_post_user(self):
        response = self.app.get("/users/john")
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        response = self.app.post("/users/john")
        self.assertEqual(response.status_code, 201)
        response = self.app.get("/users/john")
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        for g in ok.app.config["DEFAULT_GROUPS"]:
            self.assertIn(g, body["groups"])

    def test_users_url_post_user_no_auto_create(self):
        with OkConfig(NO_AUTO_CREATE):
            response = self.app.get("/users/john")
            body = json.loads(response.data)
            self.assertEqual(response.status_code, 404)
            response = self.app.post("/users/john")
            self.assertEqual(response.status_code, 201)
            response = self.app.get("/users/john")
            body = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            for g in ok.app.config["DEFAULT_GROUPS"]:
                self.assertIn(g, body["groups"])

    def test_users_url_post_user_customized_default_groups(self):
        with OkConfig(CUSTOMIZED_DEFAULT_GROUPS):
            response = self.app.get("/users/john")
            body = json.loads(response.data)
            self.assertEqual(response.status_code, 404)
            response = self.app.post("/users/john")
            self.assertEqual(response.status_code, 201)
            response = self.app.get("/users/john")
            body = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            for g in ok.app.config["DEFAULT_GROUPS"]:
                self.assertIn(g, body["groups"])

    def test_users_url_post_user_group_unrestricted_users(self):
        response = self.app.get("/users/john")
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        response = self.app.post("/users/john", data={"groups": "unrestricted"})
        self.assertEqual(response.status_code, 201)
        response = self.app.get("/users/john")
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("unrestricted", body["groups"])

    def test_users_url_post_user_unexisting_group(self):
        response = self.app.get("/groups/unexisting")
        self.assertEqual(response.status_code, 404)
        response = self.app.get("/users/john")
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        response = self.app.post("/users/john", data={"groups": "unexisting"})
        self.assertEqual(response.status_code, 201)
        response = self.app.get("/users/john")
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("unexisting", body["groups"])
        response = self.app.get("/groups/unexisting")
        self.assertEqual(response.status_code, 404)

    def test_users_url_delete_unexisting_user(self):
        response = self.app.get("/users/john")
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        response = self.app.delete("/users/john")
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 404)

    def test_users_url_delete_user(self):
        response = self.app.get("/users/john")
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.app.post("/users/john")
        response = self.app.get("/users/john")
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        response = self.app.delete("/users/john")
        self.assertEqual(response.status_code, 200)

    def test_users_url_update_unexisting_user(self):
        response = self.app.get("/users/john")
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        response = self.app.put("/users/john", data={"groups" : "doesnotmatter"})
        self.assertEqual(response.status_code, 404)
        response = self.app.get("/users/john")
        self.assertEqual(response.status_code, 404)

    def test_users_url_repost_existing_user(self):
        response = self.app.get("/users/john")
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        response = self.app.post("/users/john", data={"groups" : "group"})
        self.assertEqual(response.status_code, 201)
        response = self.app.post("/users/john", data={"groups" : "group"})
        self.assertEqual(response.status_code, 400)

    def test_users_url_update_user(self):
        response = self.app.get("/users/john")
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        response = self.app.post("/users/john", data={"groups" : "first"})
        self.assertEqual(response.status_code, 201)
        response = self.app.get("/users/john")
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.data)
        self.assertIn("first", body["groups"])
        response = self.app.put("/users/john", data={"groups" : "second"})
        self.assertEqual(response.status_code, 200)
        response = self.app.get("/users/john")
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.data)
        self.assertNotIn("first", body["groups"])
        self.assertIn("second", body["groups"])
        response = self.app.put("/users/john", data={"groups" : "third"})
        self.assertEqual(response.status_code, 200)
        response = self.app.get("/users/john")
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.data)
        self.assertNotIn("first", body["groups"])
        self.assertNotIn("second", body["groups"])
        self.assertIn("third", body["groups"])

    def test_groups_url(self):
        response = self.app.get("/groups/")
        self.assertEquals(response.status_code, 200)

    def test_groups_url_get_unknown_group(self):
        response = self.app.get("/groups/doesnotexist")
        self.assertEquals(response.status_code, 404)

    def test_groups_url_post_empty_group(self):
        response = self.app.post("/groups/emptygroup")
        self.assertEquals(response.status_code, 201)
        response = self.app.get("/groups/emptygroup")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.data), {"restrictions": []})

    def test_groups_url_post_group_twice(self):
        response = self.app.get("/groups/mygroup")
        self.assertEquals(response.status_code, 404)
        response = self.app.post("/groups/mygroup")
        self.assertEquals(response.status_code, 201)
        response = self.app.get("/groups/mygroup")
        self.assertEquals(response.status_code, 200)
        response = self.app.post("/groups/mygroup")
        self.assertEquals(response.status_code, 400)

    def test_groups_url_post_group(self):
        myrestrictions = [["/foo", "unrestricted", None],
                          ["/bar", "unrestricted", None]]
        response = self.app.post("/groups/mygroup",
                data={"restrictions": json.dumps(myrestrictions)}
                )
        self.assertEquals(response.status_code, 201)
        response = self.app.get("/groups/mygroup")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
                json.loads(response.data)["restrictions"],
                myrestrictions
                )

    def test_groups_url_post_group_unknown_restriction(self):
        myrestrictions = [["/foo", "unknownrestriction", None]]
        response = self.app.post("/groups/mygroup",
                data={"restrictions": json.dumps(myrestrictions)}
                )
        self.assertEquals(response.status_code, 400)

    def test_groups_url_put_unknown_group(self):
        response = self.app.put("/groups/doesnotexist")
        self.assertEquals(response.status_code, 404)

    def test_groups_url_put_group(self):
        response = self.app.post("/groups/mygroup")
        self.assertEquals(response.status_code, 201)
        response = self.app.get("/groups/mygroup")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.data), {"restrictions": []})
        myrestrictions = [["/foo", "unrestricted", None],
                          ["/bar", "unrestricted", None]]

        response = self.app.put("/groups/mygroup",
                data={"restrictions": json.dumps(myrestrictions)}
                )
        self.assertEquals(response.status_code, 200)
        response = self.app.get("/groups/mygroup")
        self.assertEquals(response.status_code, 200)
        body = json.loads(response.data)
        self.assertEquals(body["restrictions"], myrestrictions)

    def test_groups_url_delete_unknown_group(self):
        response = self.app.delete("/groups/unknown")
        self.assertEquals(response.status_code, 404)

    def test_groups_url_delete_group(self):
        response = self.app.post("/groups/mygroup")
        self.assertEquals(response.status_code, 201)
        response = self.app.delete("/groups/mygroup")
        self.assertEquals(response.status_code, 200)

    def test_restrictions_url(self):
        response = self.app.get("/restrictions/")
        self.assertEqual(response.status_code, 200)

    def test_restrictions_url_get_restriction(self):
        response = self.app.get("/restrictions/unrestricted")
        self.assertEqual(response.status_code, 200)

    def test_restrictions_url_get_unexisting_restriction(self):
        response = self.app.get("/restrictions/idontexist")
        self.assertEqual(response.status_code, 404)

    def test_help_urls(self):
        response = self.app.get("/help/")
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.data)
        for link in body["links"].values():
            response = self.app.get(link)
            self.assertEqual(response.status_code, 200)

    def test_help_url_unkown(self):
        response = self.app.get("/help/idontexist")
        self.assertEqual(response.status_code, 404)

    def test_ok_url_simple(self):
        response = self.app.get("/ok/?url=" + urlencode("/")
                + "&groups=unrestricted")
        self.assertEqual(response.status_code, 200)

    def test_ok_url_advanced_restrictions_user(self):
        with OkConfig(ADVANCED_RESTRICTIONS):
            myrestrictions = [
                        ["/recipes", "http_methods", ["GET"]],
                        ["/recipes", "restricted_ingredient", "fruits"]
                        ]
            response = self.app.post("/groups/fruitlovers",
                    data={"restrictions": json.dumps(myrestrictions)}
                    )
            self.assertEqual(response.status_code, 201)
            response = self.app.post("/users/john",
                    data={"groups": "fruitlovers"}
                    )
            self.assertEqual(response.status_code, 201)
            response = self.app.get("/ok/?url=" + urlencode("/somepath") +
                    "&user=john")
            self.assertEqual(response.status_code, 403)
            response = self.app.get("/ok/?url=" + urlencode("/recipes") +
                    "&user=john")
            self.assertEqual(response.status_code, 200)
            response = self.app.get("/ok/?url=" +
                    urlencode("/recipes?ingredient=eggplant") +
                    "&user=john")
            self.assertEqual(response.status_code, 403)
            response = self.app.get("/ok/?url=" +
                    urlencode("/recipes?ingredient=apple") +
                    "&groups=fruitlovers&http_method=POST")
            self.assertEqual(response.status_code, 403)
            response = self.app.get("/ok/?url=" +
                    urlencode("/recipes?ingredient=apple") +
                    "&user=john")
            self.assertEqual(response.status_code, 200)

    def test_ok_url_hint(self):
        with OkConfig(ADVANCED_RESTRICTIONS):
            myrestrictions = [
                        ["/recipes", "http_methods", ["GET"]],
                        ["/recipes", "restricted_ingredient", "fruits"]
                        ]
            response = self.app.post("/groups/fruitlovers",
                    data={"restrictions": json.dumps(myrestrictions)}
                    )
            self.assertEqual(response.status_code, 201)
            response = self.app.post("/users/john",
                    data={"groups": "fruitlovers"}
                    )
            self.assertEqual(response.status_code, 201)
            response = self.app.get("/ok/?url=" +
                    urlencode("/recipes?ingredient=apple") +
                    "&user=john")
            self.assertEqual(response.status_code, 200)
            body = json.loads(response.data)
            self.assertEqual(body,
                    {
                        u'fruitlovers':
                        [[u'/recipes', u'http_methods', [u'GET']],
                         [u'/recipes', u'restricted_ingredient', u'fruits']]
                    })

    def test_ok_url_custom_hint(self):
        with OkConfig(ADVANCED_RESTRICTIONS_CUSTOM_HINT):
            myrestrictions = [
                        ["/recipes", "http_methods", ["GET"]],
                        ["/recipes", "restricted_ingredient", "fruits"]
                        ]
            response = self.app.post("/groups/fruitlovers",
                    data={"restrictions": json.dumps(myrestrictions)}
                    )
            self.assertEqual(response.status_code, 201)
            response = self.app.post("/users/john",
                    data={"groups": "fruitlovers"}
                    )
            self.assertEqual(response.status_code, 201)
            response = self.app.get("/ok/?url=" +
                    urlencode("/recipes?ingredient=apple") +
                    "&user=john")
            self.assertEqual(response.status_code, 200)
            body = json.loads(response.data)
            self.assertEqual(body, {u'fruitlovers': True})

    def test_ok_url_advanced_restrictions_weird_username(self):
        with OkConfig(ADVANCED_RESTRICTIONS):
            myusername = urlencode(u'Émilien Jeunêt')
            myrestrictions = [
                        ["/recipes", "http_methods", ["GET"]],
                        ["/recipes", "restricted_ingredient", "fruits"]
                        ]
            response = self.app.post("/groups/fruitlovers",
                    data={"restrictions": json.dumps(myrestrictions)}
                    )
            self.assertEqual(response.status_code, 201)
            response = self.app.post("/users/" + myusername,
                    data={"groups": "fruitlovers"}
                    )
            self.assertEqual(response.status_code, 201)
            response = self.app.get("/ok/?url=" + urlencode("/somepath") +
                    "&user=" + myusername)
            self.assertEqual(response.status_code, 403)
            response = self.app.get("/ok/?url=" + urlencode("/recipes") +
                    "&user=" + myusername)
            self.assertEqual(response.status_code, 200)
            response = self.app.get("/ok/?url=" +
                    urlencode("/recipes?ingredient=eggplant") +
                    "&user=" + myusername)
            self.assertEqual(response.status_code, 403)
            response = self.app.get("/ok/?url=" +
                    urlencode("/recipes?ingredient=apple") +
                    "&groups=fruitlovers&http_method=POST")
            self.assertEqual(response.status_code, 403)
            response = self.app.get("/ok/?url=" +
                    urlencode("/recipes?ingredient=apple") +
                    "&user=" + myusername)
            self.assertEqual(response.status_code, 200)

    def test_ok_url_any_group_gets_you_access(self):
        restrictions1 = [["/path1", "http_methods", ["GET"]]]
        restrictions2 = [["/path2", "http_methods", ["GET"]]]
        response = self.app.post("/groups/group1",
                data={"restrictions": json.dumps(restrictions1)}
                )
        self.assertEqual(response.status_code, 201)
        response = self.app.post("/groups/group2",
                data={"restrictions": json.dumps(restrictions2)}
                )
        self.assertEqual(response.status_code, 201)
        response = self.app.get("/ok/?url=" + urlencode("/path1") +
                "&groups=group1")
        self.assertEqual(response.status_code, 200)
        response = self.app.get("/ok/?url=" + urlencode("/path2") +
                "&groups=group1")
        self.assertEqual(response.status_code, 403)
        response = self.app.get("/ok/?url=" + urlencode("/path1") +
                "&groups=group2")
        self.assertEqual(response.status_code, 403)
        response = self.app.get("/ok/?url=" + urlencode("/path2") +
                "&groups=group2")
        self.assertEqual(response.status_code, 200)
        response = self.app.get("/ok/?url=" + urlencode("/path2") +
                "&groups=" + urlencode("group1,group2"))
        self.assertEqual(response.status_code, 200)
        response = self.app.get("/ok/?url=" + urlencode("/path2") +
                "&groups=" + urlencode("group2,group1"))
        self.assertEqual(response.status_code, 200)

    def test_ok_url_advanced_restrictions_group(self):
        with OkConfig(ADVANCED_RESTRICTIONS):
            myrestrictions = [
                        ["/recipes", "http_methods", ["GET"]],
                        ["/recipes", "restricted_ingredient", "fruits"]
                        ]
            response = self.app.post("/groups/fruitlovers",
                    data={"restrictions": json.dumps(myrestrictions)}
                    )
            self.assertEqual(response.status_code, 201)
            response = self.app.get("/ok/?url=" + urlencode("/somepath") +
                    "&groups=fruitlovers")
            self.assertEqual(response.status_code, 403)
            response = self.app.get("/ok/?url=" + urlencode("/recipes") +
                    "&groups=fruitlovers")
            self.assertEqual(response.status_code, 200)
            response = self.app.get("/ok/?url=" +
                    urlencode("/recipes?ingredient=eggplant") +
                    "&groups=fruitlovers")
            self.assertEqual(response.status_code, 403)
            response = self.app.get("/ok/?url=" +
                    urlencode("/recipes?ingredient=apple") +
                    "&groups=fruitlovers&http_method=POST")
            self.assertEqual(response.status_code, 403)
            response = self.app.get("/ok/?url=" +
                    urlencode("/recipes?ingredient=apple") +
                    "&groups=fruitlovers")
            self.assertEqual(response.status_code, 200)

    def test_ok_url_no_url(self):
        response = self.app.post("/groups/mygroup")
        self.assertEqual(response.status_code, 201)
        response = self.app.post("/users/john",data={"groups": "mygroup"})
        self.assertEqual(response.status_code, 201)
        response = self.app.get("/ok/?user=john&group=mygroup")
        self.assertEqual(response.status_code, 400)

    def test_ok_url_anonymous(self):
        response = self.app.get("/ok/?url=" + urlencode("/"))
        self.assertEqual(response.status_code, 403)
        restrictions = [[".*", "unrestricted", None]]
        response = self.app.put("/groups/anonymous",
                data={"restrictions": json.dumps(restrictions)})
        self.assertEqual(response.status_code, 200)
        response = self.app.get("/ok/?url=" + urlencode("/"))
        self.assertEqual(response.status_code, 200)

    def test_ok_url_auto_create_user(self):
        response = self.app.get("/users/john")
        self.assertEqual(response.status_code, 404)
        restrictions = [["/public.*$", "unrestricted", None]]
        for group in ok.app.config["DEFAULT_GROUPS"]:
            response = self.app.put("/groups/%s" % group,
                    data={"restrictions": json.dumps(restrictions)}
                    )
            self.assertEqual(response.status_code, 200)
        response = self.app.get("/ok/?url=" + urlencode("/public") +
                "&user=john")
        self.assertEqual(response.status_code, 200)
        response = self.app.get("/users/john")
        self.assertEqual(response.status_code, 200)

    def test_ok_url_no_auto_create_unknown_user(self):
        with OkConfig(NO_AUTO_CREATE):
            response = self.app.get("/users/john")
            self.assertEqual(response.status_code, 404)
            restrictions = [["/public.*$", "unrestricted", None]]
            for group in ok.app.config["DEFAULT_GROUPS"]:
                response = self.app.put("/groups/%s" % group,
                        data={"restrictions": json.dumps(restrictions)}
                        )
                self.assertEqual(response.status_code, 200)
            response = self.app.get("/ok/?url=" + urlencode("/public") +
                    "&user=john")
            self.assertEqual(response.status_code, 403)
            response = self.app.get("/users/john")
            self.assertEqual(response.status_code, 404)

    def test_ok_url_unknown_group(self):
        response = self.app.get("/ok/?url=" + urlencode("/") +
                "&groups=mygroup")
        self.assertEqual(response.status_code, 403)

    def test_restriction_host_match(self):
        restrictions = [["/.*$", "host_match", "success.com"]]
        for group in ok.app.config["DEFAULT_GROUPS"]:
            response = self.app.put("/groups/%s" % group,
                    data={"restrictions": json.dumps(restrictions)}
                    )
            self.assertEqual(response.status_code, 200)
        response = self.app.get(
            "/ok/?url=" + urlencode("http://success.com/") +
            "&groups=%s" % ",".join(ok.app.config["DEFAULT_GROUPS"])
            )
        self.assertEqual(response.status_code, 200)
        response = self.app.get(
            "/ok/?url=" + urlencode("http://fail.com/") +
            "&groups=%s" % ",".join(ok.app.config["DEFAULT_GROUPS"])
            )
        self.assertEqual(response.status_code, 403)

    def test_restriction_ports(self):
        restrictions = [["/.*$","ports", [80, 443]]]
        for group in ok.app.config["DEFAULT_GROUPS"]:
            response = self.app.put("/groups/%s" % group,
                    data={"restrictions": json.dumps(restrictions)}
                    )
            self.assertEqual(response.status_code, 200)
        response = self.app.get(
            "/ok/?url=" + urlencode("http://example.com/") +
            "&groups=%s" % ",".join(ok.app.config["DEFAULT_GROUPS"])
            )
        self.assertEqual(response.status_code, 200)
        response = self.app.get(
                "/ok/?url=" + urlencode("http://example.com:80/") +
            "&groups=%s" % ",".join(ok.app.config["DEFAULT_GROUPS"])
            )
        self.assertEqual(response.status_code, 200)
        response = self.app.get(
                "/ok/?url=" + urlencode("http://example.com:443/") +
            "&groups=%s" % ",".join(ok.app.config["DEFAULT_GROUPS"])
            )
        self.assertEqual(response.status_code, 200)
        response = self.app.get(
                "/ok/?url=" + urlencode("https://example.com:444/") +
            "&groups=%s" % ",".join(ok.app.config["DEFAULT_GROUPS"])
            )
        self.assertEqual(response.status_code, 403)
        response = self.app.get(
                "/ok/?url=" + urlencode("http://example.com:81/") +
            "&groups=%s" % ",".join(ok.app.config["DEFAULT_GROUPS"])
            )
        self.assertEqual(response.status_code, 403)

    def test_restriction_http_methods(self):
        restrictions = [[".*", "http_methods", ["GET", "PUT"]]]
        for group in ok.app.config["DEFAULT_GROUPS"]:
            response = self.app.put("/groups/%s" % group,
                    data={"restrictions": json.dumps(restrictions)}
                    )
            self.assertEqual(response.status_code, 200)
        response = self.app.get(
            "/ok/?url=" + urlencode("http://example.com/") +
            "&groups=%s" % ",".join(ok.app.config["DEFAULT_GROUPS"])
            )
        self.assertEqual(response.status_code, 200)
        response = self.app.get(
            "/ok/?url=" + urlencode("http://example.com/") +
            "&groups=%s" % ",".join(ok.app.config["DEFAULT_GROUPS"]) +
            "&http_method=PUT"
            )
        self.assertEqual(response.status_code, 200)
        response = self.app.get(
            "/ok/?url=" + urlencode("http://example.com/") +
            "&groups=%s" % ",".join(ok.app.config["DEFAULT_GROUPS"]) +
            "&http_method=POST"
            )
        self.assertEqual(response.status_code, 403)

    def test_restriction_schemes(self):
        restrictions = [[".*", "schemes", ["https"]]]
        for group in ok.app.config["DEFAULT_GROUPS"]:
            response = self.app.put("/groups/%s" % group,
                    data={"restrictions": json.dumps(restrictions)}
                    )
            self.assertEqual(response.status_code, 200)
        response = self.app.get(
            "/ok/?url=" + urlencode("https://example.com/") +
            "&groups=%s" % ",".join(ok.app.config["DEFAULT_GROUPS"])
            )
        self.assertEqual(response.status_code, 200)
        response = self.app.get(
            "/ok/?url=" + urlencode("http://example.com/") +
            "&groups=%s" % ",".join(ok.app.config["DEFAULT_GROUPS"]) +
            "&http_method=PUT"
            )
        self.assertEqual(response.status_code, 403)


class DictionaryTestCase():
    """
    Generic dictionary test case, used to test the serializeddicts
    """

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

