# Fonctions qui n'ont nulle part d'autre où aller
from import_var import *

T = TypeVar('T')    # v. les types génériques (generics) dans la PEP 484
Err = TypeVar('Err')
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

def utilisateur_valide_menu(ev : pygame.event.Event) -> bool:
    return ev.type == pygame.KEYDOWN and ev.key in UI_TOUCHES_VALIDER

def testeur_skip(ev : pygame.event.Event) -> bool:
    return MODE_DEBUG and ev.type == pygame.KEYDOWN and ev.key in DBG_TOUCHES_SKIP

def attendre(secondes : float) -> None:
    intervalle = .01    # check toutes les centièmes de secondes
    for _ in range(int(secondes//intervalle)):  # arrondi au plus bas
        for ev in pygame.event.get():
            quitter_si_necessaire(ev)
            if MODE_DEBUG and testeur_skip(ev):
                return
        
        time.sleep(intervalle)
    time.sleep(secondes % intervalle)   # attend le temps restant

def pourcentage_hauteur(pourcents : int) -> int:
    """Renvoie pourcent% de la hauteur de l'écran en pixels"""
    return round(HAUTEUR * pourcents/100)

def pourcentage_largeur(pourcents : int) -> int:
    """Renvoie pourcent% de la largeur de l'écran en pixels"""
    return round(LARGEUR * pourcents/100)