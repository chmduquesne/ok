from kyotocabinet import *
import sys
import os

class KyotoCabinetDict():

    def __init__(self, path):
        db_path = path
        self.db = DB()
        if not self.db.open(db_path, DB.OWRITER | DB.OCREATE):
            raise OSError(str(self.db.error()))

    def __len__(self):
        return int(self.db.count())

    def __getitem__(self, key):
        value = self.db.get(key)
        if value is None:
            raise KeyError(str(self.db.error()))
        return value

    def __setitem__(self, key, value):
        if not self.db.set(key, value):
            raise ValueError(str(self.db.error()))

    def __delitem__(self, key):
        if not self.db.remove(key):
            raise KeyError(str(self.db.error()))

    def __iter__(self):
        for item in self.iteritems():
            yield item[0]

    def __contains__(self, item):
        return self.db.check(item) != -1

    def __delete__(self):
        if not self.db.close():
            raise OSError(str(self.db.error()))

    def has_key(self, key):
        return key in self

    def iteritems(self):
        cursor = self.db.cursor()
        cursor.jump()
        while True:
            record = cursor.get(True)
            if not record:
                break
            yield (record[0], record[1])
        cursor.disable()

    def iterkeys(self):
        for key, value in self.iteritems():
            yield key

    def itervalues(self):
        for key, value in self.iteritems():
            yield value

    def keys(self):
        return [i for i in self.iterkeys()]

    def values(self):
        return [i for i in self.itervalues()]

    def clear(self):
        for i in self.iterkeys():
            del self[i]

    def get(self, key, value=None):
        res = self.db.get(key)
        if res is None:
            return value

    def pop(self, key, default=None):
        res = self.db.get(key)
        if res is None:
            if default is None:
                raise KeyError
            else:
                return default
        del self[key]
        return res

    def items(self):
        return [i for i in self.iteritems()]

def test():
    print "create empty dict"
    db = KyotoCabinetDict("test.kch")
    print "add a=b, c=d"
    db["a"] = "b"
    db["c"] = "d"
    print "get db['a'], db['c']"
    print db["a"]
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
