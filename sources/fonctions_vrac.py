# Fonctions qui n'ont nulle part d'autre où aller
from import_var import *
from Duree import Duree
from Jeu   import Jeu

def premier_indice_libre_de_entites_vivantes() -> int:
    """Retourne le premier indice disponible dans globales.entites_vivantes[] ou -1 s'il n'y en a pas."""
    assert(len(globales.entites_vivantes) <= Constantes.MAX_ENTITES_SIMULTANEES), "Trop d'entitées sont dans le combat."
    for i in range(len(globales.entites_vivantes)):
        if globales.entites_vivantes[i] is None:
            return i
    return -1


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

def pause(temps_attente : Duree) -> Generator[bool, None, None]:
    """Renvoie `True` une fois que la `temps_attente` s'est écoulée."""
    fin : Duree = Jeu.duree_execution + temps_attente
    
    while Jeu.duree_execution < fin:
        yield False
    yield True

def attendre(temps_attente : Duree) -> None:
    """
    Fait planter le programme pendant une durée de `temps_attente`.
    La fonction n'accepte que des durées de moins d'une seconde.
    Contrairement à `pause()` qui peut s'éxécuter sur plusieurs frames, `attendre()` ne s'éxécute que sur une et une seule frame d'où de telles restrictions.
    """
    assert(temps_attente <= Duree(s=1)), "Temps d'attente trop long "
    
    Jeu.duree_execution.millisecondes += Jeu.clock.tick_busy_loop(1 / temps_attente.secondes)   # framerate = 1 / temps_execution_frame

def avancer_generateurs(gen_list : list[Generator[Any, Any, Any]], to_send : Any = None) -> None:
    """
    Appelle `next()` sur tous les générateurs de la liste.
    Si un générateur élève une `StopIteration`, l'enlève de la liste.
    """
    for i, gen in enumerate(gen_list.copy()):
        try:
            gen.send(to_send)
        except StopIteration:
            gen_list.pop(i)

def terminer_generateur(gen : Generator, a_envoyer : Any = None) -> None:
    """
    Exécute `gen` tant qu'il n'est pas fini.
    N'appelle PAS `Jeu.commencer_frame()` donc la condition de sortie ne doit pas dépendre sur une variable globale non modifiée par la fonction.
    """
    while True:
        try:
            gen.send(a_envoyer)
        except StopIteration:
            return

def terminer_interruption(gen : Interruption) -> None:
    """Exécute `gen` jusqu'à qu'il soit fini. Les résultats sont affichés à l'écran, met à jour l'horloge."""
    while True:
        Jeu.commencer_frame()
        try:
            Jeu.fenetre.blit(next(gen), (0, 0))
            pygame.display.flip()
        except StopIteration:
            return


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