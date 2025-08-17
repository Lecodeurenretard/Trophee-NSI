# Fonctions qui n'ont nulle part d'autre où aller
from import_var import *

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
    """Renvoie pourcentage de la hauteur de l'écran en pixels"""
    return round(HAUTEUR * pourcents/100)

def pourcentage_largeur(pourcents : int) -> int:
    """Renvoie pourcentage de la largeur de l'écran en pixels"""
    return round(LARGEUR * pourcents/100)