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
        for name in entry.key:
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
            name = None
            try:
                for name in key:
                    tree = tree.get(name, {})
                    dir_entry = tree.get('.')
                    if dir_entry:
                        d.setdefault('.', dir_entry)
                    d = d.setdefault(name, {})
                else:
                    if name is not None:
                        d.update(tree.get(name, {}))
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
            self.scan(name=name, path=value.path, key=list(entry.key))
