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
