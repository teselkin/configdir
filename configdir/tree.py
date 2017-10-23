from configdir.entry import Entry
from configdir.entry import EntryKey

import os


class Tree(object):
    def __init__(self, root, strict=False):
        self.strict = strict
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

    def load(self, key=None):
        """

        :param key: DatabaseEntryKey object
        :return:
        """
        result = dict()
        d = result
        tree = self._
        d.setdefault('.', tree['.'])
        name = None
        try:
            part = EntryKey('')
            for name in key:
                if name:
                    try:
                        tree = tree[name]
                    except KeyError:
                        if self.strict:
                            raise Exception("Bad key '{}' - "
                                            "name '{}' not in tree."
                                            .format(str(key), name))
                        tree = {}
                    part += EntryKey(name)
                    d = d.setdefault(name, {})
                    dir_entry = tree.get('.')
                    if dir_entry:
                        d.setdefault('.', dir_entry)
                else:
                    if self.strict:
                        raise Exception(
                            "Empty keys are not allowed in strict mode")
                    for k, v in tree.items():
                        if k.startswith('^'):
                            continue
                        if k == '.':
                            continue
                        d.setdefault(k, self.load(part + EntryKey(k)))
            else:
                if name is not None:
                    d.update(tree.get(name, {}))
        except KeyError:
            print("No DirEntry item for key '{}'".format(name))
            raise

        return result

    def scan(self, name=None, path=None, key=list()):
        entry = Entry(key=key, name=name, path=path)
        entry.scan()
        self.new(entry)

        for name, value in entry.keys.items():
            self.scan(name=name, path=value.path, key=list(entry.key))
