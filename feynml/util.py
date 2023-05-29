def len_not_none(arr):
    """
    Length of a List/tuple ignoring None values (e.g. regex non matches at the end)

    Example

    >>> len_not_none((1,2,3,None))
    3
    >>> len_not_none([1,2,3,None])
    3
    """
    i = 0
    for a in arr:
        if a is not None:
            i += 1
    return i
