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
    def __init__(self, name=None, path=None):
        self.name = name
        self.path = path
        self.keys = dict()
        self.files = dict()
        self.data = dict()
        self.patterns = dict()

    def scan(self):
        for x in os.scandir(str(self.path)):
            if x.is_dir():
                self.keys[x.name] = x
            else:
                self.files[x.name] = x

        if 'data.yaml' in self.files:
            with open(self.files['data.yaml'].path) as f:
                data = yaml.load(f, Loader=yaml.BaseLoader)

            for key, value in data.items():
                if str(key).startswith('^'):
                    self.patterns[key] = value
                else:
                    self.keys[key] = None

        for name, entry in self.keys.items():
            if entry:
                yield name, entry.path

    def load(self, whitelist=None):
        data = dict()
        if 'data.yaml' in self.files:
            with open(self.files['data.yaml'].path) as f:
                data.update(yaml.load(f, Loader=yaml.BaseLoader))

        keys = list()
        if whitelist:
            for name in self.keys:
                if name in whitelist:
                    keys.append(name)
        else:
            keys.extend(self.keys)

        for name in keys:
            data.setdefault(name, {})
            self.data[name] = data.get(name, {})

        return data

    def dict(self):
        data = dict()
        data.update(self.data)
        for key in self.keys:
            data.setdefault(str(key), {})

        for pattern, value in self.patterns.items():
            data.setdefault(pattern, value)

        return data
