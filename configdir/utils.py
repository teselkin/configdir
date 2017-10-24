import re

re_any = re.compile(r'^.*$')


def merge_dict(d1, d2):
    if not isinstance(d1, dict):
        return

    if not isinstance(d2, dict):
        return

    for k2, v2 in d2.items():
        if isinstance(v2, dict):
            d1.setdefault(k2, dict())
            merge_dict(d1[k2], v2)
        elif isinstance(v2, list):
            d1.setdefault(k2, list())
            for x in reversed(v2):
                d1[k2].insert(0, x)
        else:
            d1[k2] = v2

    return


def expand_dict(d1, recursive=False):
    if not isinstance(d1, dict):
        return

    patterns = list()
    for k, v in d1.items():
        if str(k).startswith('^'):
            if isinstance(v, dict):
                patterns.append(k)
            else:
                raise Exception(
                    "Values for regexp matching should be dict, not {}: "
                    "{}".format(type(v).__name__, {k: v}))

    if '^.*$' in patterns:
        d1.setdefault('*', {})

    for x in range(len(patterns)):
        pattern = patterns[x]
        patterns[x] = (re.compile(pattern), d1.pop(pattern))

    for k, v in d1.items():
        for pattern, value in patterns:
            if pattern.match(k):
                merge_dict(v, value)

    if recursive:
        for value in d1.values():
            expand_dict(value, recursive=recursive)

    return
