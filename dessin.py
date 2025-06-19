from Attaque import *

def dessiner_barre_de_vie(pos_x : int, pos_y : int, ratio_vie : float, longueur_remplissage : int) -> None:
    couleur_remplissage : color = VERT

    if ratio_vie <= .2:
        couleur_remplissage = ROUGE
    elif ratio_vie <= .5:
        couleur_remplissage = JAUNE
    
    pygame.draw.rect(fenetre, couleur_remplissage   , (pos_x  , pos_y  , longueur_remplissage      , 10), 0)
    pygame.draw.rect(fenetre, NOIR                  , (pos_x-1, pos_y-1, UI_LONGUEUR_BARRE_DE_VIE+2, 11), 2)

def dessiner_nom(nom : str, position : pos) -> None:
    # c'est plus clair de mettre cette ligne en procédure
    fenetre.blit(variables_globales.POLICE_GRAND.render(nom, True, NOIR), position)

def dessiner_bouttons_attaques() -> None:
    # Dessiner les boites
    pygame.draw.rect(fenetre, BLANC, (70 , (13 * HAUTEUR // 16) - 25, 200, 50), 5) # soin
    pygame.draw.rect(fenetre, BLANC, (70 , (13 * HAUTEUR // 16) + 45, 200, 50), 5) # torgnole
    pygame.draw.rect(fenetre, BLANC, (375, (13 * HAUTEUR // 16) - 25, 200, 50), 5) #...
    pygame.draw.rect(fenetre, BLANC, (375, (13 * HAUTEUR // 16) + 45, 200, 50), 5)
    
    # Dessiner les noms
    fenetre.blit(ATTAQUES_DISPONIBLES["heal"].get_nom_surface()    , (140, (13 * HAUTEUR // 16) - 12))
    fenetre.blit(ATTAQUES_DISPONIBLES["physique"].get_nom_surface(), (120, (13 * HAUTEUR // 16) + 60))
    fenetre.blit(ATTAQUES_DISPONIBLES["magie"].get_nom_surface()   , (400, (13 * HAUTEUR // 16) - 12))