from import_var import *
from Pos import Pos
from Duree import Duree

def dessiner_rect(
        surface : Surface,
        position : tuple[int, int]|Pos, dimensions : tuple[int, int]|list[int],
        couleur_remplissage : color = ROUGE, couleur_bords : color = NOIR,
        epaisseur_trait : int = 1, dessiner_interieur : bool = True,
        centre_x : bool = False, centre_y : bool = False,
    ) -> None:
    if type(position) is tuple:
        position = Pos(position)
    assert(type(position) is Pos)   # c'est censé être sûr mais Pylance ne le pense pas
    
    if centre_x:
        position.x -= dimensions[0] // 2
    if centre_y:
        position.y -= dimensions[1] // 2
    
    if dessiner_interieur:
        pygame.draw.rect(
            surface,
            couleur_remplissage,
            (
                position.x, position.y,
                dimensions[0], dimensions[1]
            )
        )
    
    if epaisseur_trait > 0:
        pygame.draw.rect(
            surface,
            couleur_bords,
            (
                position.x, position.y,
                dimensions[0], dimensions[1]
            ),
            width=epaisseur_trait
        )

def dessiner_barre_de_vie(surface : Surface, pos_x : int, pos_y : int, ratio_vie : float, longueur_remplissage : int) -> None:
    from parametres_vars import mode_debug
    
    if mode_debug.case_cochee:
        dessiner_rect(surface, (pos_x, pos_y), (longueur_remplissage, UI_HAUTEUR_BARRE_DE_VIE), GRIS, epaisseur_trait=0)
        dessiner_rect(surface, (pos_x, pos_y), (UI_LONGUEUR_BARRE_DE_VIE, UI_HAUTEUR_BARRE_DE_VIE), couleur_bords=NOIR, epaisseur_trait=2, dessiner_interieur=False)
        return
    
    couleur_remplissage : rgb = VERT
    if ratio_vie <= .2:
        couleur_remplissage = ROUGE
    elif ratio_vie <= .5:
        couleur_remplissage = JAUNE
    
    dessiner_rect(surface, (pos_x, pos_y), (longueur_remplissage, UI_HAUTEUR_BARRE_DE_VIE), couleur_remplissage=couleur_remplissage, epaisseur_trait=0)
    dessiner_rect(surface, (pos_x, pos_y), (UI_LONGUEUR_BARRE_DE_VIE, UI_HAUTEUR_BARRE_DE_VIE), couleur_bords=NOIR, epaisseur_trait=2, dessiner_interieur=False)

def dessiner_nom(nom : str, position : Pos) -> None:
    # c'est plus clair de mettre cette ligne en procédure
    fenetre.blit(globales.POLICE_TITRE.render(nom, True, NOIR), tuple(position))

def image_vers_generateur(image : Surface, temps_affichage : Duree) -> Generator[Surface, None, None]:
    """
    Renvoie un générateur qui renvoie `image` pendant le temps requis.
    """
    fin : Duree = globales.temps_de_jeu + temps_affichage
    while globales.temps_de_jeu < fin:
        yield image