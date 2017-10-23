import os
import yaml


class EntryPath(object):
    def __init__(self, path, sep=None):
        self.sep = sep or os.sep
        self._ = self.split(path)

    def __str__(self):
        return self.sep.join(self.elements)

    def split(self, path):
        if isinstance(path, str):
            elements = path.split(self.sep)
        elif isinstance(path, list):
            elements = path
        else:
            raise Exception("Bad input path '{}' - type '{}' unsupported"
                            .format(path, type(path)))

        for x in reversed(range(len(elements))):
            if not elements[x]:
                elements.pop(x)

        return elements

    @property
    def elements(self):
        return [x for x in self._]

class EntryKey(object):
    def __init__(self, key, subkey=None, sep=None):
        self.sep = sep or ':'
        if isinstance(key, list):
            self._ = []
            self._.extend(key)
        else:
            self._ = self.split(key)
        if subkey:
            self._.extend(self.split(subkey))

    def __iter__(self):
        for x in self._:
            yield x

    def __add__(self, other):
        elements = []
        for name in self:
            elements.append(name)
        for name in other:
            elements.append(name)
        return EntryKey(elements)

    def __str__(self):
        return self.sep.join(self._)

    def split(self, key):
        if key:
            if isinstance(key, str):
                elements = key.split(self.sep)
            elif isinstance(key, list):
                elements = key
            else:
                raise Exception("Bad input key '{}' - type '{}' unsupported"
                                .format(key, type(key)))
        else:
            elements = list()

        return elements


class Entry(object):
    def __init__(self, name=None, path=None, key=list(), sep=os.sep):
        self.name = name
        self.keys = dict()
        self.files = dict()
        self.data = dict()
        self.key = EntryKey(key=key, subkey=name)
        self.path = EntryPath(path=path, sep=sep)

    def scan(self):
        """
        Scan directory entry
        Return tuple of dictionaries
            dirs
              key: key name (might not be equal to directory name)
              value: OsEntry element for next entry
            files
              key: file name
              value: OsEntry element for that file
        :param path:
        :return:
        """
        self.files = dict()
        self.keys = dict()
        for x in os.scandir(str(self.path)):
            if x.is_dir():
                self.keys[x.name] = x
            else:
                self.files[x.name] = x

    def load(self, whitelist=None):
        data = dict()
        if 'data.yaml' in self.files:
            data.update(yaml.load(open(self.files['data.yaml'].path)))

        keys = list()
        if whitelist:
            for name in self.keys:
                if name in whitelist:
                    keys.append(name)
        else:
            keys.extend(self.keys)

        for name in keys:
            data.setdefault(name, {})

        return data

    def dict(self):
        return dict()

    def tree(self):
        tree = dict()
        for x in self.keys.keys():
            tree.setdefault(x, {})
        return tree
