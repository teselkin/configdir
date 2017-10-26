from configdir.tree import Tree
from configdir.entry import EntryKey
from configdir.utils import merge_dict
from configdir.utils import expand_dict

import yaml


class ConfigDir(object):
    def __init__(self, path, strict=True):
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
        for child in tree:
            child.scan()
            for x in self.iterate(child, keys + [child.name, ]):
                yield x
        yield keys

    def dict(self, key, recursive=True, expand=True):
        if isinstance(key, str):
            key = EntryKey(key)

        tree = self.root.select(key)
        keys = [None, ]
        for x in key:
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

        return data[None]

    def get(self, key, recursive=True):
        if isinstance(key, str):
            key = EntryKey(key)

        data = self.dict(key, recursive=recursive)

        for name in key:
            try:
                data = (data.get(name) or data['*'])
            except KeyError:
                if self.strict:
                    raise Exception("Bad key '{}' - '{}' not found"
                        .format(str(key), name))
                else:
                    return {}

        return data

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
