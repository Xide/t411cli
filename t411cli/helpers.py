def sanitize(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to underscores.
    :param value: unsafe string
    :return safe string
    """
    from re import sub
    from unicodedata import normalize
    value = normalize('NFKD', value).encode('ascii', 'ignore')
    value = sub('[^\w\s\.-]', '', value.decode('utf-8')).strip().lower()
    return sub('[-_\s]+', '_', value)


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)
