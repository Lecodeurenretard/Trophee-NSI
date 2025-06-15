# Fonctions qui n'ont nulle part d'autre où aller

def find(list: list | tuple, elem, error_value : int | float = -1) -> int | float:	# elem: any
    """
    Find the first occurence of elem in list, if not found return `error_value` (only case where the function can return a float).
    """
    try:
        return list.index(elem)
    except:
        return error_value

assert(find([1, 2, 3, 4], 3) == 2)  # Quelques tests
assert(find([1, 2, 3, 4], 1) == 0)
assert(find([1, 2, 3, 4], 5) == -1)
assert(find([1, 2, 3, 4], 5, 42) == 42)