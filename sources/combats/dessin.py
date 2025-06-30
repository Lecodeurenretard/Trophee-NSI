from import_var import *

def dessine_barre_de_vie(surface : Surface, pos_x : int, pos_y : int, ratio_vie : float, longueur_remplissage : int) -> None:
    couleur_remplissage : color = VERT

    if ratio_vie <= .2:
        couleur_remplissage = ROUGE
    elif ratio_vie <= .5:
        couleur_remplissage = JAUNE
    
    pygame.draw.rect(surface, couleur_remplissage   , (pos_x  , pos_y  , longueur_remplissage      , 10), 0)
    pygame.draw.rect(surface, NOIR                  , (pos_x-1, pos_y-1, UI_LONGUEUR_BARRE_DE_VIE+2, 11), 2)

def dessiner_nom(nom : str, position : Pos) -> None:
    # c'est plus clair de mettre cette ligne en procédure
    fenetre.blit(variables_globales.POLICE_GRAND.render(nom, True, NOIR), tuple(position))