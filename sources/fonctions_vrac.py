# Fonctions qui n'ont nulle part d'autre où aller
from import_var import *
from Duree import Duree

def premier_indice_libre_de_entites_vivantes() -> int:
    """Retourne le premier indice disponible dans globales.entites_vivantes[] ou -1 s'il n'y en a pas."""
    assert(len(globales.entites_vivantes) <= MAXIMUM_ENTITES_SIMULTANEES), "Trop d'entitées sont dans le combat."
    for i in range(len(globales.entites_vivantes)):
        if globales.entites_vivantes[i] is None:
            return i
    return -1

# Le système d'overload est à la fois une bénédiction pour la fonctionnalité
# et une malédiction pour sa syntaxe.
@overload
def verifier_pour_quitter() -> None:
    """
    Vérifie si un évènement dans la file des evènements est un évènement permettant de sortir, s'il en existe un quitte immédiatement.
    Vide la file des évènements.
    La décision est prise par la version surchargée avec un évènement.
    """
    ...

@overload
def verifier_pour_quitter(ev : pygame.event.Event) -> None:
    """
    Vérifie si `ev` permet de quitter le jeu, il doit respecter au moins une de ces conditions:
    - Être de type `pygame.QUIT`;
    - Représenter l'appui de la touche `TOUCHE_QUITTER`.
    """
    ...

def verifier_pour_quitter(ev : Optional[pygame.event.Event] = None) -> None:
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
    assert(len(dest) >= 2), "On attend que le paramètre `dest` aie au moins 2 éléments."
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
    from parametres_vars import mode_debug
    
    return mode_debug.case_cochee and ev.type == pygame.KEYDOWN and ev.key in DBG_TOUCHES_SKIP

@overload
def testeur_skip_ou_quitte() -> bool:
    """
    Vérifie si un évènement dans la file des evènements est un évènement permettant de sortir, s'il en existe un quitte immédiatement.
    La fonction vérifie aussi si le testeur veut skip, dans ce cas là elle renvoie `True`.
    Vide la file des évènements.
    La décision est prise par la version avec un argument.
    """
    ...
@overload
def testeur_skip_ou_quitte(ev : pygame.event.Event) -> bool:
    """
    Vérifie si `ev` permet de quitter le jeu, il doit respecter au moins une de ces conditions:
    - Être de type `pygame.QUIT`;
    - Représenter l'appui de la touche `TOUCHE_QUITTER`.
    
    La fonction vérifie aussi si le testeur veut skip dans ce cas là elle renvoie `True`.
    """
    ...

def testeur_skip_ou_quitte(ev : Optional[pygame.event.Event] = None) -> bool:
    if ev is not None:
        verifier_pour_quitter(ev)
        return testeur_skip(ev)
    
    for ev in pygame.event.get():
        if testeur_skip_ou_quitte(ev):
            return True
    return False

def pause(temps_attente : Duree) -> Generator[bool, None, None]:
    """Renvoie `True` une fois que la `temps_attente` s'est écoulée."""
    fin : Duree = globales.temps_de_jeu + temps_attente
    
    while globales.temps_de_jeu < fin:
        yield False
    yield True



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
    return couleur                   # type: ignore

def avancer_generateurs(gen_list : list[Generator], to_send : Any = None) -> None:
    """
    Appelle `next()` sur tous les générateurs de la liste.
    Si un générateur élève une `StopIteration`, l'enlève de la liste.
    """
    for i, gen in enumerate(reversed(gen_list)):
        try:
            gen.send(to_send)
        except StopIteration:
            gen_list.pop(i)

def terminer_generateur(gen : Generator, a_envoyer : Any = None) -> None:
    """
    Exécute `gen` tant qu'il n'est pas fini.
    N'appelle PAS `commencer_frame()` donc la condition de sortie ne doit pas dépendre sur une variable globale non modifiée par la fonction.
    """
    while True:
        try:
            gen.send(a_envoyer)
        except StopIteration:
            return

def terminer_interruption(gen : Interruption) -> None:
    """Exécute `gen` jusqu'à qu'il soit fini. Les résultats sont affichés à l'écran, met à jour l'horloge."""
    while True:
        commencer_frame()
        try:
            fenetre.blit(next(gen), (0, 0))
            pygame.display.flip()
        except StopIteration:
            return

def commencer_frame(framerate : int = 60) -> None:
    """La fonction à appeler à chaque début de frame."""
    globales.temps_de_jeu.millisecondes += clock.tick(framerate)


@overload
def centrer_pos_tuple(pos : tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    """Centre la tuple de rectangle: `(pos_en_x, pos_en_y, taille_en_x, taille_en_y)` comme si c'était un rectangle."""
    ...

@overload
def centrer_pos_tuple(pos : tuple[int, int], dim : tuple[int, int]) -> tuple[int, int]:
    """Centre la tuple de position: `(pos_en_x, pos_en_y)` comme si c'était un rectangle de dimensions `(taille_en_x, taille_en_y)`."""
    ...

def centrer_pos_tuple(pos : tuple[int, int, int, int]|tuple[int, int], dim : Optional[tuple[int, int]] = None) -> tuple[int, int, int, int]|tuple[int, int]:
    if len(pos) == 4:
        return (
            pos[0] - pos[2] // 2,
            pos[1] - pos[3] // 2,
            pos[2], pos[3]
        )
    
    assert(dim is not None), "Il y a un bug dans les overloads"
    return (pos[0] - dim[0] // 2, pos[1] - dim[1] // 2)




def changer_etat(nouvel_etat : EtatJeu) -> None:
    """Change l'état du jeu vers `nouvel_etat`."""
    globales.precedent_etat_jeu = globales.etat_jeu
    globales.etat_jeu           = nouvel_etat