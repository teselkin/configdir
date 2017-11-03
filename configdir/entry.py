import re
import yaml

try:
    from os import scandir
except ImportError:
    from scandir import scandir


re_quoted = re.compile(r'%([A-Fa-f0-9]{2})')


class EntryKey(object):
    def __init__(self, key, subkey=None, sep=None):
        self.sep = sep or '|'
        if isinstance(key, list):
            self._ = [x.lower() for x in key]
        else:
            self._ = self.split(key.lower())
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
        self.special = {
            '_any_': '*',
        }

    def scan(self):
        for x in scandir(str(self.path)):
            if x.is_dir():
                name = self.unquote(x.name)
                self.keys[self.special.get(name, name)] = x
            else:
                self.files[x.name] = x

        if 'data.yaml' in self.files:
            with open(self.files['data.yaml'].path) as f:
                data = yaml.load(f, Loader=yaml.BaseLoader)

            if data:
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

    def unquote(self, value):
        return re_quoted.sub(lambda m: chr(int(m.group(1), 16)), value)

