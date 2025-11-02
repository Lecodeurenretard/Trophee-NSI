# Fonctions qui n'ont nulle part d'autre où aller
from import_var import *
from Jeu import Jeu
from classes_utiles.Animation import valeurs_regulieres_entre_01

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
            Jeu.display_flip()
        except StopIteration:
            return


@overload
def centrer_pos(pos : tuple[int, int, int, int], *, centrer_x : bool = True, centrer_y : bool = True) -> tuple[int, int, int, int]:
    """Centre la tuple de rectangle: `(pos_en_x, pos_en_y, taille_en_x, taille_en_y)` comme si c'était un rectangle."""
    ...
@overload
def centrer_pos(pos : tuple[int, int], dim : tuple[int, int], *, centrer_x : bool = True, centrer_y : bool = True) -> tuple[int, int]:
    """Centre la tuple de position: `(pos_en_x, pos_en_y)` comme si c'était un rectangle de dimensions `(taille_en_x, taille_en_y)`."""
    ...
@overload
def centrer_pos(pos : Pos, dim : tuple[int, int], *, centrer_x : bool = True, centrer_y : bool = True) -> Pos:
    """Centre la tuple de position: `(pos_en_x, pos_en_y)` comme si c'était un rectangle de dimensions `(taille_en_x, taille_en_y)`."""
    ...

def centrer_pos(
            pos : tuple[int, int, int, int]|tuple[int, int]|Pos,
            dim : Optional[tuple[int, int]] = None,
            *,  # necessaire pour que l'overload marche
            centrer_x : bool = True,
            centrer_y : bool = True,
    ) -> tuple[int, int, int, int]|tuple[int, int]|Pos:
    if type(pos) is Pos:
        assert(dim is not None), "Il y a un bug dans les overloads"
        return centrer_pos(pos, dim, centrer_x=centrer_x, centrer_y=centrer_y)
    
    assert(type(pos) is tuple)  # reassuring the type checker
    if len(pos) == 4:
        return (
            pos[0] - pos[2] // 2 if centrer_x else pos[0] ,
            pos[1] - pos[3] // 2 if centrer_y else pos[1] ,
            pos[2], pos[3]
        )
    
    assert(dim is not None), "Il y a un bug dans les overloads"
    return (
        pos[0] - dim[0] // 2 if centrer_x else pos[0] ,
        pos[1] - dim[1] // 2 if centrer_y else pos[1] 
    )

def valeurs_regulieres(minimum : float, maximum : float, nombre_a_produire : int, inclure_min : bool = True, inclure_max : bool = False) -> list[float]:
    """`valeurs_regulieres_entre_01()` mais entre `minimum` et `maximum`."""
    res = valeurs_regulieres_entre_01(nombre_a_produire, inclure_0=inclure_min, inclure_1=inclure_max)
    return [val * (maximum - minimum) + minimum for val in res]     # J'aime pas voir des lerp partout.

def dessiner_texte(
            surface : Surface,
            texte : str,
            couleur : color,
            espace_ecriture : tuple[int, int, int, int]|list[int],
            police : pygame.font.Font,
            aa : bool = False,
            ecart_entre_lignes : int = -2,
            arriere_plan : Optional[color] = None,
            dessiner_boite : bool = False,
    ) -> str:
    """
    Dessine le texter `surface` en le gardant dans `rect`. Il sera de couleur `couleur` et de police `police`. Si le texte est trop long ou est trop grand, ne blit que le début.
    `aa` décide de l'antialiasing (paramètre `antialias` de `pygame.Font.render()`).
    `ecart_entre_lignes` s'occupe de l'écart entre les lignes, il n'est pas absolu et ne n'est qu'ajouté à un écart préexisant.
    `arriere_plan` contient la couleur d'arrière plan au None, si le paramètre est None, ne dessine pas d'arrère plan.
    
    Renvoie le texte non dessiné.
    
    La fonction originale vient du wiki Pygame: https://www.pygame.org/wiki/TextWrap
    """
    rect : Rect = Rect(espace_ecriture)
    y    : int = rect.top
    
    hauteur_police = police.size("Tg")[1]
    
    while len(texte) != 0:
        dernier_index_a_render : int = 1
        
        # Détermine si la ligne sort de l'aire prédéfinie.
        if y + hauteur_police > rect.bottom:
            break
        
        # Vérifie s'il y a un saut de ligne dans le texte
        position_saut = texte.find("\n")
        
        # Détermine la longueur maximum de la ligne
        while police.size(texte[:dernier_index_a_render])[0] < rect.width and dernier_index_a_render < len(texte):
            dernier_index_a_render += 1
        
        # Si on trouve un \n avant la fin de la ligne, on coupe là
        if position_saut != -1 and position_saut < dernier_index_a_render:
            dernier_index_a_render = position_saut + 1
        # Si on a bien wrap le texte, on fini la ligne au dernier mot
        elif dernier_index_a_render < len(texte): 
            dernier_index_a_render = texte.rfind(" ", 0, dernier_index_a_render) + 1
        
        # Render la ligne (sans le \n)
        ligne_a_render = texte[:dernier_index_a_render].rstrip("\n")
        if arriere_plan is not None:
            image = police.render(ligne_a_render, True, couleur, arriere_plan)
            image.set_colorkey(arriere_plan)
        else:
            image = police.render(ligne_a_render, aa, couleur)
        
        # Dessine la ligne sur la surface
        surface.blit(image, (rect.left, y))
        y += hauteur_police + ecart_entre_lignes
        
        # Enlève le texte que l'on vient de dessiner
        texte = texte[dernier_index_a_render:]
    
    if dessiner_boite:
        pygame.draw.rect(surface, ROUGE, espace_ecriture, 2)
    
    return texte

def translation(rect : Rect, v : Vecteur) -> Rect:
    """Translate le rectangle `rect` par le vecteur `v`."""
    return Rect(rect.left + v.x, rect.top + v.y, rect.width, rect.height)