from import_var import *

def demander_pseudo():
    pseudo = ""
    saisie = True
    font = pygame.font.SysFont(None, 48)
    while saisie:
        fenetre.fill(BLANC)
        texte = font.render("Entrez votre pseudo :", True, NOIR)
        fenetre.blit(texte, (LARGEUR // 2 - 180, HAUTEUR // 2 - 60))
        pseudo_affiche = font.render(pseudo, True, BLEU)
        fenetre.blit(pseudo_affiche, (LARGEUR // 2 - 100, HAUTEUR // 2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(pseudo) > 0:
                    saisie = False
                elif event.key == pygame.K_BACKSPACE:
                    pseudo = pseudo[:-1]
                else:
                    if len(pseudo) < 12 and event.unicode.isprintable():
                        pseudo += event.unicode
    return pseudo



def afficher_info():
    curseur_empl = get_curseur_emplacement()
    if curseur_empl == (0, 0):
        info = variables_globales.police_ecriture.render("Puissance: 0,5", True, NOIR)
        info2 = variables_globales.police_ecriture.render("Soigner-vous de quelque pv ", True, NOIR)
        fenetre.fill(BLANC)
        fenetre.blit(info, (3*(LARGEUR//10), (HAUTEUR//2)))
        fenetre.blit(info2, (3*(LARGEUR//10)-100, (HAUTEUR//2)+30))
        pygame.display.flip()
        time.sleep(2)
        return
    
    if curseur_empl == (0, 1):
        info = variables_globales.police_ecriture.render("Puissance: 20", True, NOIR)
        info2 = variables_globales.police_ecriture.render("Infligez des dégâts physiques à l'adversaire", True, NOIR)
        fenetre.fill(BLANC)
        fenetre.blit(info, (3*(LARGEUR//10), (HAUTEUR//2)))
        fenetre.blit(info2, (3*(LARGEUR//10)-100, (HAUTEUR//2)+30))
        pygame.display.flip()
        time.sleep(2)
        return




def chargement():
    barre = 0
    while barre < 700:
        fenetre.fill(BLANC)
        pygame.draw.rect(fenetre, NOIR, (50, 300, barre, 50), 0)
        texte_chargement = police_ecriture.render("Chargement...", True, NOIR)
        fenetre.blit(texte_chargement, (300, 350))
        pygame.display.flip()
        barre += 2
        time.sleep(0.01)
        pygame.event.clear()

def afficher_nombre_combat(nbr_combat):
    texte_combat = police_ecriture.render(f"Combat n°{nbr_combat}", True, NOIR)
    fenetre.fill(BLANC)
    fenetre.blit(texte_combat, (LARGEUR // 2 - 100, HAUTEUR // 2 - 20))
    pygame.display.flip()
    time.sleep(2)

def dessiner_barre_de_vie(pos_x, pos_y, vie_actuelle, vie_max, longueur_remplissage):
    couleur_remplissage = VERT
    if vie_actuelle < vie_max / 5:
        couleur_remplissage = ROUGE
    elif vie_actuelle < vie_max / 2:
        couleur_remplissage = JAUNE
    pygame.draw.rect(fenetre, couleur_remplissage, (pos_x, pos_y , longueur_remplissage, 10), 0)
    
    pygame.draw.rect(fenetre, NOIR, (pos_x-1, pos_y-1 , UI_LONGUEUR_BARRE_DE_VIE+2, 11), 2)

def dessiner_nom(nom, position):
    # c'est plus clair de mettre cette ligne en procédure
    fenetre.blit(police_ecriture.render(nom, True, NOIR), position)


def rafraichir_ecran():
    # Effacer l'écran en redessinant l'arrière-plan
    fenetre.fill(BLANC)


    # Redessiner les éléments fixes (par exemple, les rectangles)
    pygame.draw.rect(fenetre, NOIR                      , (    0            , 3 * HAUTEUR // 4      , 800, 600), 0)
    pygame.draw.rect(fenetre, BLEU                      , (    LARGEUR // 4 , 3 * HAUTEUR // 4 - 100, 100, 100), 0)
    pygame.draw.rect(fenetre, variables_globales.couleur, (6 * LARGEUR // 10,     HAUTEUR // 4 - 100, 100, 100), 0)

    pygame.draw.rect(fenetre, BLANC, (70 , (13 * HAUTEUR // 16) - 25, 200, 50), 5) # soin
    pygame.draw.rect(fenetre, BLANC, (70 , (13 * HAUTEUR // 16) + 45, 200, 50), 5) # torgnole
    pygame.draw.rect(fenetre, BLANC, (375, (13 * HAUTEUR // 16) - 25, 200, 50), 5)
    pygame.draw.rect(fenetre, BLANC, (375, (13 * HAUTEUR // 16) + 45, 200, 50), 5)

    dessiner_barre_de_vie(50, 50, variables_globales.monstre_vie, variables_globales.monstre_stat["vie"], variables_globales.barre_vie_remplie_monstre)
    dessiner_barre_de_vie(500, 400, variables_globales.joueur_vie, variables_globales.joueur_stat["vie"], variables_globales.barre_vie_remplie_joueur)

    dessiner_nom(variables_globales.nom_adversaire, (49, 20))
    dessiner_nom(variables_globales.pseudo_joueur, (499, 370))

    # Dessiner le cercle à la nouvelle position
    pygame.draw.circle(fenetre, VERT, (variables_globales.curseur_x, variables_globales.curseur_y), 10, 0)

    # Afficher nom des attaques
    fenetre.blit(texte_soin         , (140, (13 * (HAUTEUR // 16)) - 12))
    fenetre.blit(texte_torgnole     , (120, (13 * (HAUTEUR // 16)) + 60))
    fenetre.blit(texte_magique      , (400, (13 * (HAUTEUR // 16)) - 12))
    fenetre.blit(texte_input_ligne1 , (620, (13 * (HAUTEUR // 16)) - 12))
    fenetre.blit(texte_input_ligne2 , (620, (13 * (HAUTEUR // 16)) + 20))


    # Mettre à jour l'affichage
    pygame.display.flip()

def get_curseur_emplacement():
    """
    Retourne une tuple caractérisant la position du curseur si le curseur n'est à aucune position connue, met un NaN sur la coordonée correspondante.

    Exemples:
    prenons
        curseur_pos_attendue_x = (60, 80)
        curseur_pos_attendue_y = (70, 90)
    et
        variables_globales.curseur_x = 60
        variables_globales.curseur_y = 90
    
    alors quelle_position_curseur() retournera (0, 1)
    

    Si cette fois
        variables_globales.curseur_x = 61
        variables_globales.curseur_y = 70
    
    alors quelle_position_curseur() retournera (NAN, 0)
    """
    alias_x = variables_globales.curseur_pos_attendue_x     # N'utilise pas de mémoire supplémentaire
    alias_y = variables_globales.curseur_pos_attendue_y     # v. les références implicites en python

    res_x = NAN
    for i in range(len(alias_x)):
        if variables_globales.curseur_x == alias_x[i]:
            res_x = i
            break
    
    res_y = NAN
    for i in range(len(alias_y)):
        if variables_globales.curseur_y == alias_y[i]:
            res_y = i
            break
    
    return (res_x, res_y)
