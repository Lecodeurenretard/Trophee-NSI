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
    except ValueError:
        return error_value

assert(find([1, 2, 3, 4], 3) == 2)  # Quelques tests
assert(find([1, 2, 3, 4], 1) == 0)
assert(find([1, 2, 3, 4], 5) == -1)
assert(find([1, 2, 3, 4], 5, 42) == 42)



def premier_indice_libre_de_entitees_vivantes() -> int:
    """Retourne le premier indice disponible dans entitees_vivantes[] ou -1 s'il n'y en a pas."""
    for i in range(len(entitees_vivantes)):
        if entitees_vivantes[i] is None:
            return i
    return -1

def quitter_si_necessaire(ev : pygame.event.Event) -> None:
    if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
        quit()