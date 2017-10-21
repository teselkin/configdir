from configdir.entry import Entry

import os


class Tree(object):
    def __init__(self, root):
        self._ = dict()
        self.root = root
        self.sep = os.sep
        self.keysep = ':'

    def new(self, entry):
        d = self._
        for name in entry.key.elements:
            d = d.setdefault(name, {})
        d.setdefault('.', entry)

    def __str__(self):
        return str(self._)

    def dict(self, key=None):
        """

        :param key: DatabaseEntryKey object
        :return:
        """
        result = dict()
        if key:
            d = result
            tree = self._
            d.setdefault('.', tree['.'])
            try:
                for name in key.elements[:-1]:
                    tree = tree.get(name, {})
                    d.setdefault('.', tree['.'])
                    d = d.setdefault(name, {})
                for name in key.elements[-1:]:
                    d.setdefault('.', tree['.'])
                    d.setdefault(name, tree.get(name, {}))
            except KeyError:
                print("No DirEntry item for key '{}'".format(name))
                raise
        else:
            result.update(self._)
        return result

    def scan(self, name=None, path=None, key=list()):
        entry = Entry(key=key, name=name, path=path)
        entry.scan()
        self.new(entry)

        for name, value in entry.keys.items():
            self.scan(name=name, path=value.path, key=entry.key.elements)
