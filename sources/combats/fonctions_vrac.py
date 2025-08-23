# Fonctions qui n'ont nulle part d'autre où aller
from import_var import *

def premier_indice_libre_de_entites_vivantes() -> int:
    """Retourne le premier indice disponible dans globales.entites_vivantes[] ou -1 s'il n'y en a pas."""
    assert(len(globales.entites_vivantes) <= MAXIMUM_ENTITES_SIMULTANEES), "Trop d'entitées sont dans le combat."
    for i in range(len(globales.entites_vivantes)):
        if globales.entites_vivantes[i] is None:
            return i
    return -1

def quitter_si_necessaire(ev : pygame.event.Event) -> None:
    if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
        quit()

def verifier_pour_quitter() -> None:
    for ev in pygame.event.get():
        quitter_si_necessaire(ev)

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
    """Renvoie pourcentage de la hauteur de l'écran en pixels"""
    return round(HAUTEUR * pourcents/100)

def pourcentage_largeur(pourcents : int) -> int:
    """Renvoie pourcentage de la largeur de l'écran en pixels"""
    return round(LARGEUR * pourcents/100)