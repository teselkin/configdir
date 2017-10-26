from configdir.entry import Entry

from configdir.utils import merge_dict


class Tree(object):
    def __init__(self, name=None, parent=None, entry=None):
        self.name = name
        self.parent = parent
        self._children = dict()
        self.entry = entry

    @classmethod
    def root(cls, path):
        return Tree(entry=Entry(path=path))

    def add_child(self, item):
        self._children[item.name] = item

    def __iter__(self):
        for x in self._children.values():
            yield x

    def scan(self, recursive=False):
        for name, path in self.entry.scan():
            entry = Entry(name=name, path=path)
            self.add_child(Tree(name=name, parent=self, entry=entry))
        if recursive:
            for child in self:
                child.scan(recursive=recursive)

    def child(self, name):
        return self._children.get(name)

    def children(self, name=None):
        children = list()
        if name:
            child = self.child('*')
            if child:
                children.append(child)
            if name != '*':
                child = self.child(name)
                if child:
                    children.append(child)
        else:
            children.extend(self._children.values())
        return children

    def select(self, key):
        tree = [[self, ], ]
        for name in key:
            children = list()
            for item in tree[-1]:
                for child in item.children(name):
                    child.scan()
                    children.append(child)
            if children:
                tree.append(children)

        for child in tree[-1]:
            child.scan(recursive=True)

        return tree

    def dict(self, recursive=False):
        data = dict()
        self.entry.load()
        merge_dict(data, self.entry.dict())
        for x in self:
            d = data.setdefault(x.name, {})
            if recursive:
                merge_dict(d, x.dict(recursive=recursive))
        return data
