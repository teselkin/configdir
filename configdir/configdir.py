from configdir.tree import Tree
from configdir.entry import EntryKey
from configdir.utils import merge_dict
from configdir.utils import expand_dict


class ConfigDir(object):
    def __init__(self, path, strict=True):
        self.root = Tree.root(path=path)
        self.strict = strict
        self.root.scan()

    def dict(self, key, recursive=True, expand=True):
        if isinstance(key, str):
            key = EntryKey(key)

        tree = self.root.select(key)

        data = dict()
        d = data
        x = None
        for x in tree:
            d = d.setdefault(x.name, {})
            merge_dict(d, x.dict())
        else:
            if recursive:
                if x:
                    merge_dict(d, x.dict(recursive=True))

        if expand:
            expand_dict(data, recursive=True)

        return data

    def get(self, key, recursive=True):
        if isinstance(key, str):
            key = EntryKey(key)

        data = self.dict(key, recursive=recursive)
        d = data[None]

        for name in key:
            try:
                d = (d.get(name) or d['*'])
            except KeyError:
                if self.strict:
                    raise Exception("Bad key '{}' - '{}' not found"
                        .format(str(key), name))
                else:
                    return {}

        return d

    def getall(self, recursive=True):
        data = dict()
        self.root.scan()
        xdict = self.root.dict()
        merge_dict(data, xdict)

        for x in self.root:
            x.scan(recursive=recursive)
            xdict = x.dict(recursive=recursive)
            merge_dict(data.setdefault(x.name, {}), xdict)

        expand_dict(data, recursive=True)

        return data
