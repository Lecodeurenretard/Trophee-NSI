# Fonctions qui n'ont nulle part d'autre où aller
from import_var import *

T = TypeVar('T')    # Generics in the PEP 484
Err = TypeVar('Err')    # Generics in the PEP 484
def find(list: list[T] | tuple[T, ...], elem : T, error_value : Err = -1) -> int | Err:	# elem: any
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