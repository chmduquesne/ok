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

