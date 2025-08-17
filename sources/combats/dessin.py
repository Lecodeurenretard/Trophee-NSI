from import_var import *
    
def _dessine_rect_barre_de_vie(surface: Surface, couleur_remplissage, pos_x : int, pos_y : int, longueur_remplissage : int, epaisseur_trait : int) -> None:
    pygame.draw.rect(
        surface,
        couleur_remplissage,
        (
            pos_x,
            pos_y,
            longueur_remplissage,
            UI_HAUTEUR_BARRE_DE_VIE
        )
    )
    pygame.draw.rect(
        surface,
        NOIR,
        (
            pos_x - epaisseur_trait // 2,
            pos_y - epaisseur_trait // 2,
            UI_LONGUEUR_BARRE_DE_VIE + epaisseur_trait,
            UI_HAUTEUR_BARRE_DE_VIE + epaisseur_trait // 2
        ),
        epaisseur_trait
    )

def dessine_barre_de_vie(surface : Surface, pos_x : int, pos_y : int, ratio_vie : float, longueur_remplissage : int) -> None:
    if MODE_DEBUG:
        _dessine_rect_barre_de_vie(surface, GRIS, pos_x, pos_y, longueur_remplissage, 2)
        return
    
    couleur_remplissage : color = VERT

    if ratio_vie <= .2:
        couleur_remplissage = ROUGE
    elif ratio_vie <= .5:
        couleur_remplissage = JAUNE
    _dessine_rect_barre_de_vie(surface, couleur_remplissage, pos_x, pos_y, longueur_remplissage, 2)

def dessiner_nom(nom : str, position : Pos) -> None:
    # c'est plus clair de mettre cette ligne en procédure
    fenetre.blit(globales.POLICE_TITRE.render(nom, True, NOIR), tuple(position))