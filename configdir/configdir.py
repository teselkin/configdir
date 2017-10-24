from configdir.tree import Tree
from configdir.entry import EntryKey
from configdir.utils import merge_dict
from configdir.utils import expand_dict


class ConfigDir(object):
    def __init__(self, path, strict=True):
        self.root = Tree.root(path=path)
        self.strict = strict
        self.root.scan()

    def get(self, key):
        if isinstance(key, str):
            key = EntryKey(key)

        tree = self.root.select(key)

        data = dict()
        d = data
        x = None
        for x in tree:
            d = d.setdefault(x.name, {})
            xdict = x.dict()
            merge_dict(d, xdict)
        else:
            if x:
                xdict = x.dict(recursive=True)
                merge_dict(d, xdict)

        expand_dict(data, recursive=True)

        d = data[None]

        for name in key:
            try:
                d = d[name]
            except KeyError:
                if self.strict:
                    raise Exception("Bad key '{}' - '{}' not found"
                        .format(str(key), name))
                else:
                    return {}

        return d

    def getall(self):
        data = dict()
        self.root.scan(recursive=True)
        xdict = self.root.dict()
        merge_dict(data, xdict)

        for x in self.root:
            xdict = x.dict(recursive=True)
            merge_dict(data.setdefault(x.name, {}), xdict)

        expand_dict(data, recursive=True)

        return data
