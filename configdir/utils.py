import re

re_any = re.compile(r'^.*$')


def merge_dict(lval, rval, replace=True):
    if not isinstance(lval, dict):
        return

    if not isinstance(rval, dict):
        return

    for rval_key, rval_value in rval.items():
        if isinstance(rval_value, dict):
            lval.setdefault(rval_key, dict())
            merge_dict(lval[rval_key], rval_value)
        elif isinstance(rval_value, list):
            lval.setdefault(rval_key, list())
            for x in reversed(rval_value):
                lval[rval_key].insert(0, x)
        else:
            if replace:
                lval[rval_key] = rval_value
            else:
                lval.setdefault(rval_key, rval_value)


def expand_dict(lval, recursive=False, expand_pattern=False):
    if not isinstance(lval, dict):
        return

    patterns = list()
    keys = list(lval.keys())
    for key in keys:
        if str(key).startswith('^'):
            if key == '^.*$':
                lval.setdefault('*', {})
            if expand_pattern:
                value = lval.pop(key)
                if isinstance(value, dict):
                    patterns.append((re.compile(key, re.IGNORECASE), value))
                else:
                    raise Exception(
                        "Values for regexp matching should be dict, not {}: "
                        "{}".format(type(value).__name__, {key: value}))

    for lval_key, lval_value in lval.items():
        if lval_key != '*':
            merge_dict(lval_value, lval.get('*', {}), replace=False)

        if expand_pattern:
            for pattern, value in patterns:
                m = pattern.match(lval_key)
                if m:
                    merge_dict(lval_value, value, replace=False)
                    merge_dict(lval_value, m.groupdict(), replace=False)

    if recursive:
        for value in lval.values():
            expand_dict(value, recursive=True, expand_pattern=expand_pattern)
