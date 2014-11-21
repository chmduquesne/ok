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

class KyotoCabinetDict():
    """
    KyotoCabinet database with an (incomplete) interface of dictionary
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

    def iterkeys(self):
        return self.__iter__()

    def itervalues(self):
        for key, value in self.iteritems():
            yield value

    def has_key(self, key):
        return key in self

    def keys(self):
        return list(self.iterkeys())

    def values(self):
        return list(self.itervalues())

    def items(self):
        return list(self.iteritems())

    def clear(self):
        for i in self.iterkeys():
            del self[i]

    def viewitems(self):
        raise NotImplementedError

    def viewkeys(self):
        raise NotImplementedError

    def viewvalues(self):
        raise NotImplementedError

    def copy(self):
        raise NotImplementedError

    @classmethod
    def fromkeys(cls, seq, value=None):
        raise NotImplementedError

    def setdefault(self, key, default=None):
        raise NotImplementedError

    def update(self, other):
        raise NotImplementedError

def print_kyotocabinetdict(db):
    print '{'
    for k in db:
        v = db[k]
        print '    %s (%s): %s (%s)' % (k, type(k), v, type(v))
    print '}'

def test():
    print "create empty dict"
    db = KyotoCabinetDict("test.kch")
    print_kyotocabinetdict(db)
    print "add a=b, c=d"
    db["a"] = { "key": "value" }
    db["c"] = "d"
    print_kyotocabinetdict(db)
    print "%s => %s" % ("a", db["a"])
    print "%s => %s" % ("c", db["c"])
    print "length of db"
    print len(db)
    print "deleting key c, showing length"
    del db["c"]
    print len(db)
    print "re-deleting key c, showing error"
    try:
        del db["c"]
    except KeyError:
        print "getting KeyError"
    print "Checking if a in keys"
    if "a" in db:
        print "yes"
    else:
        print "no"
    print "readding c=d"
    db["c"] = "d"

    print "iterating on keys"
    for key in iter(db):
        print key
    print "iterating on keys and values"
    for k, v in db.iteritems():
        print k, v
    print "again, on keys and values with items"
    for k, v in db.items():
        print k, v
    print "getting unexisting key, or '<missing>'"
    print db.get("missing", '<missing>')
    print "clearing db, showing len"
    db.clear()
    print len(db)

if __name__ == "__main__":
    test()
