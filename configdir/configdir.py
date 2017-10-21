from configdir.tree import Tree
from configdir.entry import EntryKey

import os
import re


class ConfigDir(object):
    def __init__(self, root=None):
        self.root = root
        self._tree = Tree(self.root)

    def open(self):
        if os.path.exists(self.root):
            self._tree.scan(path=self.root)

    def get(self, key=None, keystr=''):
        """

        :param key: EntryKey object
        :return:
        """
        if key is None:
            key = EntryKey(keystr)
        data = self.dict(key)
        for name in key.elements:
            data = data.get(name, {})
        return data

    def load(self, path):
        pass

    def dict(self, key=None, keystr=''):
        """

        :param key: EntryKey object
        :return:
        """
        result = {}
        if key is None:
            key = EntryKey(keystr)

        d = result
        tree = self._tree.dict(key)
        for name in key.elements:
            entry = tree.get('.')
            if entry:
                self.merge_data(d, entry.load(whitelist=[name, ]))
            d = d.get(name, {})
            tree = tree.get(name, {})

        entry = tree.get('.')
        if entry:
            self.merge_data(d, entry.load())

        d = result
        for name in key.elements:
            d = d.setdefault(name, {})
        self.expand_data(result)

        return result

    def merge_data(self, d1, d2):
        if not isinstance(d1, dict):
            return

        if not isinstance(d2, dict):
            return

        for k2, v2 in d2.items():
            if isinstance(v2, dict):
                d1.setdefault(k2, dict())
                self.merge_data(d1[k2], v2)
            elif isinstance(v2, list):
                d1.setdefault(k2, list())
                for x in reversed(v2):
                    d1[k2].insert(0, x)
            else:
                d1[k2] = v2

    def expand_data(self, d1):
        if not isinstance(d1, dict):
            return

        patterns = list()
        for k, v in d1.items():
            if k.startswith('^'):
                if isinstance(v, dict):
                    patterns.append(k)
                else:
                    raise Exception(
                        "Values for regexp matching should be dict, not {}: "
                        "{}".format(type(v).__name__, {k: v}))

        for x in range(len(patterns)):
            pattern = patterns[x]
            patterns[x] = (re.compile(pattern), d1.pop(pattern))

        for k, v in d1.items():
            for pattern, value in patterns:
                if pattern.match(k):
                    self.merge_data(v, value)

        for value in d1.values():
            self.expand_data(value)
