# -*- coding: utf-8 -*-

from __future__ import with_statement
from kyotocabinet import *
import json
import sys
import os


class DBOpen():
    """
    Allows to perform cleanly an operation on a KyotoCabinet database:

        >>> with DBOpen("example.kch") as db:
        >>>     print db.count()

    This will open the database before the operation, and close it after.
    """
    def __init__(self, path, mode=DB.OREADER):
        self.path = path
        self.db = None
        self.mode = mode

    def __enter__(self):
        self.db = DB()
        if not self.db.open(self.path, self.mode | DB.OCREATE):
            raise OSError(str(self.db.error()))
        return self.db

    def __exit__(self, type, value, traceback):
        if not self.db.close():
            raise OSError(str(self.db.error()))


class KyotoCabinetDict(dict):
    """
    KyotoCabinet database with an interface of dictionary
    """

    def __init__(self, path):
        self.path = path
        with DBOpen(self.path, mode=DB.OWRITER) as db:
            pass

    def __len__(self):
        with DBOpen(self.path) as db:
            return int(db.count())

    def __getitem__(self, key):
        with DBOpen(self.path) as db:
            db_key = json.dumps(key)
            db_value = db.get(db_key)
            if db_value is None:
                raise KeyError(str(db.error()))
            return json.loads(db_value)

    def __setitem__(self, key, value):
        with DBOpen(self.path, mode=DB.OWRITER) as db:
            db_key = json.dumps(key)
            db_value = json.dumps(value)
            if not db.set(db_key, db_value):
                raise ValueError(str(db.error()))

    def __delitem__(self, key):
        with DBOpen(self.path, mode=DB.OWRITER) as db:
            db_key = json.dumps(key)
            if not db.remove(db_key):
                raise KeyError(str(db.error()))

    def __contains__(self, key):
        with DBOpen(self.path) as db:
            db_key = json.dumps(key)
            return db.check(db_key) != -1

    def iteritems(self):
        with DBOpen(self.path) as db:
            cursor = db.cursor()
            cursor.jump()
            while True:
                record = cursor.get(True)
                if not record:
                    break
                db_key = record[0]
                db_value = record[1]
                key = json.loads(db_key)
                value = json.loads(db_value)
                yield (key, value)
            cursor.disable()

    def get(self, key, value=None):
        with DBOpen(self.path) as db:
            db_key = json.dumps(key)
            db_value = db.get(db_key)
            if db_value is None:
                return value
            else:
                return json.loads(db_value)

    def pop(self, key, default=None):
        with DBOpen(self.path, mode=DB.OWRITER) as db:
            db_key = json.dumps(key)
            db_value = db.get(db_key)
            if db_value is None:
                if default is None:
                    raise KeyError
                else:
                    return default
            del self[key]
            return json.loads(db_value)

    def __iter__(self):
        for key, value in self.iteritems():
            yield key

    def clear(self):
        for key in self:
            del self[key]

    def has_key(self, key):
        return key in self


class JsonDict(dict):

    def save_to_disk(self):
        with open(self.path, "wb") as f:
            json.dump(self, indent=4, fp=f)

    def __init__(self, path):
        self.path = path
        if not os.path.exists(path):
            self.save_to_disk()
        with open(self.path) as f:
            self.update(json.load(f))

    def __setitem__(self, *args, **kwargs):
        res = super(JsonDict, self).__setitem__(*args, **kwargs)
        self.save_to_disk()
        return res

    def __delitem__(self, *args, **kwargs):
        res = super(JsonDict, self).__delitem__(*args, **kwargs)
        self.save_to_disk()
        return res

    def pop(self, *args, **kwargs):
        res = super(JsonDict, self).pop(*args, **kwargs)
        self.save_to_disk()
        return res

    def clear(self, *args, **kwargs):
        res = super(JsonDict, self).clear(*args, **kwargs)
        self.save_to_disk()
        return res
