from configdir.tree import Tree
from configdir.entry import EntryKey
from configdir.utils import merge_dict
from configdir.utils import expand_dict

import yaml


class ConfigDir(object):
    def __init__(self, path, strict=False):
        self.path = path
        self.root = Tree.root(path=self.path)
        self.strict = strict
        self.schema = list()
        self.scan()

    def __iter__(self):
        for x in self.iterate(self.root):
            if x:
                yield x

    def scan(self):
        self.root.scan()
        if 'metadata.yaml' in self.root.entry.files:
            with open(self.root.entry.files['metadata.yaml'].path) as f:
                metadata = yaml.load(f, Loader=yaml.BaseLoader)
                self.schema.extend(metadata.get('schema', []))

    def iterate(self, tree, keys=list()):
        last = True
        for child in tree:
            last = False
            child.scan()
            for x in self.iterate(child, keys + [child.name, ]):
                yield x
        if last:
            yield keys

    def result(self, key, data={}):
        result = dict()
        result.update(data)
        result['__meta__'] = {
                'key': list(key),
                'schema': list(self.schema),
                'is_empty': len(data) == 0,
            }
        return result


    def dict(self, key, recursive=True, expand=True):
        if isinstance(key, str):
            entry_key = EntryKey(key)
        else:
            entry_key = key

        tree = self.root.select(entry_key)
        keys = [None, ]
        for x in entry_key:
            keys.append(x)

        data = dict()
        d = data
        items = list()
        for key, items in zip(keys, tree):
            for x in items:
                merge_dict(d.setdefault(x.name, {}), x.dict())
            expand_dict(d, expand_pattern=expand)
            d = d.setdefault(key, {})
        else:
            if recursive:
                for x in items:
                    merge_dict(d, x.dict(recursive=True))
                expand_dict(d, recursive=True, expand_pattern=expand)

        if expand:
            expand_dict(data, recursive=True, expand_pattern=True)

        return self.result(entry_key, data[None])

    def get(self, key, recursive=True):
        if isinstance(key, str):
            entry_key = EntryKey(key)
        else:
            entry_key = key

        data = self.dict(entry_key, recursive=recursive)

        for name in entry_key:
            try:
                data = (data.get(name) or data['*'])
            except KeyError:
                if self.strict:
                    raise Exception("Bad key '{}' - '{}' not found"
                        .format(str(entry_key), name))
                else:
                    return self.result(entry_key)

        return self.result(entry_key, data)

    def match(self, key):
        if isinstance(key, str):
            entry_key = EntryKey(key)
        else:
            entry_key = key

        data = self.dict(entry_key, expand=False)

        d = data
        for name in entry_key:
            d.setdefault(name, {})
            expand_dict(d, recursive=False, expand_pattern=False)
            d = d[name]

        d = data
        for name in entry_key:
            expand_dict(d, recursive=False, expand_pattern=True)
            d = d[name]
        expand_dict(d, recursive=True, expand_pattern=True)

        return self.result(entry_key, d)

    def getall(self, recursive=True):
        data = dict()
        self.root.scan()
        xdict = self.root.dict()
        merge_dict(data, xdict)

        for x in self.root:
            x.scan(recursive=recursive)
            xdict = x.dict(recursive=recursive)
            merge_dict(data.setdefault(x.name, {}), xdict)

        expand_dict(data, recursive=True, expand_pattern=True)

        return data
