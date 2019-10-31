
def size_formatter(b):
    """
    >>> size_formatter(2048)
    '2.0KB'
    >>> size_formatter(82374748)
    '82.4MB'
    >>> size_formatter(95494495843)
    '95.5GB'

    in: int
    out: str
    desc: returns string representation of bytes
    """
    if b < 1000:
        return '%i' % b + 'B'
    elif 1000 <= b < 1000000:
        return '%.1f' % float(b/1000) + 'KB'
    elif 1000000 <= b < 1000000000:
        return '%.1f' % float(b/1000000) + 'MB'
    elif 1000000000 <= b < 1000000000000:
        return '%.1f' % float(b/1000000000) + 'GB'
    elif 1000000000000 <= b:
        return '%.1f' % float(b/1000000000000) + 'TB'


def cgi_field_storage_to_dict(field_storage):
    """
    in: cgi.FieldStorage object instance
    out: dict()
    desc: parses the keys and values of an FieldStorage instance to a dict()
    """
    params = {}
    for key in field_storage.keys():
        params[key] = field_storage[key].value
    return params
