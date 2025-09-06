# Fonctions qui n'ont nulle part d'autre où aller
from import_var import *

def premier_indice_libre_de_entites_vivantes() -> int:
    """Retourne le premier indice disponible dans globales.entites_vivantes[] ou -1 s'il n'y en a pas."""
    assert(len(globales.entites_vivantes) <= MAXIMUM_ENTITES_SIMULTANEES), "Trop d'entitées sont dans le combat."
    for i in range(len(globales.entites_vivantes)):
        if globales.entites_vivantes[i] is None:
            return i
    return -1


def verifier_pour_quitter(ev : pygame.event.Event|None = None) -> None:
    """Si ev n'est pas None, pop toutes les évènements de la file d'évènements sinon vérifie si l'utilisateur veut quitter."""
    if ev is not None:
        if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.key == TOUCHE_QUITTER):
            quit()
        return
    
    for event in pygame.event.get():
        verifier_pour_quitter(event)



def blit_centre(
        toile : Surface, a_dessiner : Surface,
        dest : list[int]|tuple[int, int]|tuple[int, int, int, int],
        area : list[int]|tuple[int, int, int, int]|None = None,
        centre_en_x : bool = True, centre_en_y : bool = True,
        flags : int = 0
    ) -> Rect:
    """
    Blit `a_dessiner` sur `toile` avec les flags `flags` de façon à ce que le centre de `a_dessiner` soit aux coordonées indiquées par `dest`.
    `dest` doit contenir au moins deux éléments (seuls les deux premiers serons utilisés); sous peine d'une `AssertionError`.
    Le paramètre
    """
    assert(len(dest) >= 2 ), "On attend que le paramètre `dest` aie au moins 2 éléments."
    assert(area is None or len(area) == 4), "On attend que le paramètre `area` soit None ou aie exactement 4 éléments."
    
    emplacement_dessin : list[int] = list(dest)
    
    if centre_en_x:
        if area is not None:
            emplacement_dessin[0] -= area[2] // 2
        else:
            emplacement_dessin[0] -= a_dessiner.get_width() // 2
    
    if centre_en_y:
        if area is not None:
            emplacement_dessin[1] -= area[3] // 2
        else:
            emplacement_dessin[1] -= a_dessiner.get_height() // 2
    
    return toile.blit(a_dessiner, emplacement_dessin, area=area, special_flags=flags)



def utilisateur_valide_menu(ev : pygame.event.Event) -> bool:
    """Vérifie si l'utilisateur valide dans un menu."""
    return ev.type == pygame.KEYDOWN and ev.key in UI_TOUCHES_VALIDER

def testeur_skip(ev : pygame.event.Event) -> bool:
    """Si en mode débug, le testeur veut skip."""
    from settings_vars import mode_debug
    
    return mode_debug.case_cochee and ev.type == pygame.KEYDOWN and ev.key in DBG_TOUCHES_SKIP



def attendre(secondes : float, intervalle : float = .01) -> None:
    """Attend `secondes`s et vérifie tous les `intervalle`s si l'utilisateur veut quitter, si oui quitte."""
    from settings_vars import mode_debug    # import local pour éviter d'éventuels imports circulaires
    
    for _ in range(int(secondes//intervalle)):  # arrondi au plus bas
        for ev in pygame.event.get():
            verifier_pour_quitter(ev)
            if mode_debug.case_cochee and testeur_skip(ev):
                return
        
        time.sleep(intervalle)
    time.sleep(secondes % intervalle)   # attend le temps restant



def pourcentage_hauteur(pourcents : float) -> int:
    """Renvoie pourcentage de la hauteur de l'écran en pixels"""
    return round(HAUTEUR * pourcents / 100)

def pourcentage_largeur(pourcents : float) -> int:
    """Renvoie pourcentage de la largeur de l'écran en pixels"""
    return round(LARGEUR * pourcents / 100)



def rgb_to_rgba(couleur : rgb, nouvelle_transparence : int = 255) -> rgba:
    """Convertit une couleur RGB en RGBA. La transparence a donner à la nouvelle couleur est `nouvelle_transparence`."""
    return (*couleur, nouvelle_transparence)

def rgba_to_rgb(couleur : rgba) -> rgb:
    """Convertit une couleur RGBA en RGB en effaçant sa donnée de transparence (Souvent interprété comme si la couleur est opaque)."""
    return (couleur[0], couleur[1], couleur[2])

def color_to_rgba(couleur : color, nouvelle_transparence : int = 255) -> rgba:
    """Cette fonction est pour éviter les longues ternaires et ne pas calmer le vérifieur de types: si necessaire, elle appelle rgb_to_rgba()"""
    if type(couleur) is rgb:
        return rgb_to_rgba(couleur, nouvelle_transparence)  # type: ignore
    return couleur                                          # type: ignore

def color_to_rgb(couleur : color) -> rgba:
    """Cette fonction est pour éviter les longues ternaires et ne pas calmer le vérifieur de types: si necessaire, elle appelle rgba_to_rgb()"""
    if type(couleur) is rgba:
        return rgba_to_rgb(couleur)  # type: ignore
    return couleur                                          # type: ignore