
def lookup(data, key, default=...):
    """Look up a value in nested data structures using dot notation."""
    current = data

    for part in key.split('.'):
        try:
            if part.isdigit():
                current = current[int(part)]
            elif hasattr(current, '__getitem__'):
                current = current[part]
            else:
                current = getattr(current, part)
        except (KeyError, IndexError, AttributeError):
            if default is ...:
                raise KeyError(key)
            return default

    return current
