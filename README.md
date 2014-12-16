<!-- vim: set fileencoding=utf-8 -->

OK
==

[![Build Status](https://travis-ci.org/chmduquesne/ok.svg?branch=master)](https://travis-ci.org/chmduquesne/ok)
[![Coverage Status](https://img.shields.io/coveralls/chmduquesne/ok.svg)](https://coveralls.io/r/chmduquesne/ok?branch=master)

Ok is a webservice allowing to plug users and permissions on top of other
webservices. It is meant to be hooked to a reverse proxy such as nginx. It
exposes the url "/ok/", to which you can pass another url and a username.
It then processes some rules in order to tell whether the user can access
the given url.

Concepts
--------

Ok builds on 3 concepts: users, groups, and restrictions. Users are part
of groups, groups are subject to restrictions, and restrictions apply to
urls. When an url is processed, it examined group by group.  If for one
group, all of the restrictions apply, then the user is granted access to
the url (the webservice returns 200). Otherwise, it returns an appropriate
error code.

Ok is a framework
-----------------

Ok defines a few builtin restrictions. However, the strength of the ok is
that it can import user-defined restrictions, such that the rights can be
as complicated as they need to be. You want to define restrictions based
on a business concept? Write a python function in the config file, and it
will be automatically available.

Display hints
-------------

What ok can't do for your webservices is modify how the interface should
look like for users who have different rights. However, it can help you
by returning a display hint. Whenever ok authorizes a request, it returns
a customizable json string that your webservices can use to modify their
behavior.

Status
------

* ✔ Rest API to manage users, groups and restrictions
* ✔ User-defined restrictions automatically loaded from the config file
* ✔ Extended test suite
* ✘ GUI for managing users and groups
* ✘ Embedded tester for checking that changes don't introduce regressions
* ✘ Extended documentation

Usage
-----

Installation:

    git clone https://github.com/chmduquesne/ok.git
    python setup.py install

Note: To make packaging easier, ok can load a virtualenv at startup. It
will try to load the virtualenv from the environment variable
PYTHON_VIRTUALENV.

Define some restrictions:

    # File ~/ok_config.py
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
    """
    Restrict the ingredient argument to a given category
    """
    category = restriction_params
    if "ingredient" in http_query:
        return http_query["ingredient"] in categories[category]
    return True

Launch ok:

    export OK_CONFIG="~/ok_config.py"
    ok-serve

Create the group fruitlovers. `http_methods` is a builtin restriction, while
`restricted_ingredients` was user-defined.

    curl http://localhost:8080/groups/fruitlovers -X POST                       \
        --data 'restrictions=[["/recipes", "http_methods", ["GET"]],            \
                              ["/recipes", "restricted_ingredient", "fruits"]]'

Create the user john in fruitlovers:

    curl http://localhost:8080/users/john -X POST                       \
        --data 'groups=fruitlovers'

Check that john can get recipes with fruits, but not veggies:

    curl http://localhost:8080/ok/?url=%2Frecipes%3Fingredient%3Dbanana&user=john
    (returns 200)

    curl http://localhost:8080/ok/?url=%2Frecipes%3Fingredient%3Deggplant&user=john
    (returns 403)

Note: Ok will come with a GUI to make the management easier.
