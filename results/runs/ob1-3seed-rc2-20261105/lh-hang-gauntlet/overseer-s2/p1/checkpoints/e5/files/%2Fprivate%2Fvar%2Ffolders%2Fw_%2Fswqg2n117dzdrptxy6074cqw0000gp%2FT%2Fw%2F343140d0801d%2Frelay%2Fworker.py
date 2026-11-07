"""Split work into batches for the relay workers."""


def chunks(items, size):
    """Split items into lists of at most size items, in order."""
    return [items[i:i + size] for i in range(0, len(items) - size, size)]
