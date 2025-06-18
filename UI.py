from fonctions_vrac import *
from Joueur import *

def demander_pseudo() -> str:
    pseudo : str  = ""
    saisie : bool = True
    texte : pygame.Surface = variables_globales.POLICE_GRAND.render("Entrez votre pseudo :", True, NOIR)
    while saisie:
        pseudo, continuer = texte_entree_event(pseudo)
        if not continuer:
            break

        fenetre.fill(BLANC)
        fenetre.blit(texte, (LARGEUR // 2 - 180, HAUTEUR // 2 - 60))
        
        pseudo_affiche : pygame.Surface = variables_globales.POLICE_GRAND.render(pseudo, True, BLEU)
        fenetre.blit(pseudo_affiche, (LARGEUR // 2 - 100, HAUTEUR // 2))
        
        pygame.display.flip()
    return pseudo

def texte_entree_event(texte : str) -> tuple[str, bool]:
    continuer : bool = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type != pygame.KEYDOWN:
            continue
        
        if event.key == pygame.K_RETURN and len(texte) > 0:
            continuer = False
            continue
        if event.key == pygame.K_BACKSPACE:
            texte = texte[:-1]
            continue
        if len(texte) < 12 and event.unicode.isprintable():
            texte += event.unicode
            continue
    return (texte, continuer)


def afficher_info() -> None:
    curseur_empl : tuple[int|NaN, int|NaN]= get_curseur_emplacement()
    texte_info1 : pygame.Surface
    texte_info2 : pygame.Surface
    
    if math.isnan(curseur_empl[0]) or math.isnan(curseur_empl[1]):
        print(f"Position du curseur: {(variables_globales.curseur_x, variables_globales.curseur_y)}")
        raise ValueError("Le curseur n'est pas à un emplacement autorisé.")
    
    if curseur_empl == (0, 0):
        texte_info1 = variables_globales.POLICE_GRAND.render(f"Puissance: {variables_globales.att_soin_puissance}", True, NOIR)
        texte_info2 = variables_globales.POLICE_GRAND.render("Soigner-vous de quelque pv", True, NOIR)
    
    if curseur_empl == (1, 0):
        texte_info1 = variables_globales.POLICE_GRAND.render(f"Puissance: {variables_globales.att_magique_puissance}", True, NOIR)
        texte_info2 = variables_globales.POLICE_GRAND.render("Infligez des dégâts magique à l'adversaire", True, NOIR)
    
    if curseur_empl == (0, 1):
        texte_info1 = variables_globales.POLICE_GRAND.render(f"Puissance: {variables_globales.att_charge_puissance}", True, NOIR)
        texte_info2 = variables_globales.POLICE_GRAND.render("Infligez des dégâts physiques à l'adversaire", True, NOIR)
    
    if curseur_empl == (1, 1):
        texte_info1 = variables_globales.POLICE_GRAND.render("Puissance: 0", True, NOIR)
        texte_info2 = variables_globales.POLICE_GRAND.render("Passez votre tour.", True, NOIR)
    
    fenetre.fill(BLANC)
    
    fenetre.blit(texte_info1, (3 * LARGEUR // 10      , HAUTEUR // 2))
    fenetre.blit(texte_info2, (3 * LARGEUR // 10 - 100, HAUTEUR // 2 + 30))
    
    pygame.display.flip()
    time.sleep(2)





def chargement(duree : float = 7.0) -> None:
    barre : int = 0
    NB_ITERATION : int = 700
    while barre < NB_ITERATION:
        fenetre.fill(BLANC)
        
        pygame.draw.rect(fenetre, NOIR, (50, 300, barre, 50), 0)
        
        texte_chargement : pygame.Surface = variables_globales.POLICE_GRAND.render("Chargement...", True, NOIR)
        fenetre.blit(texte_chargement, (300, 350))
        
        pygame.display.flip()
        
        barre += 2
        time.sleep(duree / NB_ITERATION)    # On assume que toutes les actions de la boucle sont instantanées

def afficher_nombre_combat(nbr_combat : int) -> None:
    texte_combat : pygame.Surface = variables_globales.POLICE_GRAND.render(f"Combat n°{nbr_combat}", True, NOIR)

    fenetre.fill(BLANC)
    fenetre.blit(texte_combat, (LARGEUR // 2 - 100, HAUTEUR // 2 - 20))

    pygame.display.flip()
    time.sleep(2)


def rafraichir_ecran() -> None:
    # Effacer l'écran en redessinant l'arrière-plan
    fenetre.fill(BLANC)
    
    # Dessiner le fond de l'interface
    pygame.draw.rect(fenetre, NOIR, (0, 3 * HAUTEUR // 4, 800, 600), 0)
    
    # Dessiner les personnages (joueur + monstre)
    pygame.draw.rect(fenetre, BLEU                              , (    LARGEUR // 4 , 3 * HAUTEUR // 4 - 100, 100, 100), 0)
    pygame.draw.rect(fenetre, variables_globales.couleur_monstre, (6 * LARGEUR // 10,     HAUTEUR // 4 - 100, 100, 100), 0)
    
    if variables_globales.monstre_stat.est_initialise:
        dessiner_barre_de_vie(50, 50, variables_globales.monstre_stat.vie / variables_globales.monstre_stat.vie_max, variables_globales.barre_vie_remplie_monstre)

    joueur.dessiner_barre_de_vie(500, 400)
    
    dessiner_nom(variables_globales.nom_adversaire, (49, 20))
    dessiner_nom(variables_globales.pseudo_joueur, (499, 370))
    
    # Dessiner le cercle à la nouvelle position
    pygame.draw.circle(fenetre, VERT, (variables_globales.curseur_x, variables_globales.curseur_y), 10, 0)
    
    # Dessiner le texte
    fenetre.blit(TEXTE_INFO_UTILISER    , (620, (13 * HAUTEUR // 16) - 12))
    fenetre.blit(TEXTE_INFO_INFO        , (620, (13 * HAUTEUR // 16) + 20))
    
    dessiner_bouttons_attaques()
    
    # Mettre à jour l'affichage
    pygame.display.flip()

def get_curseur_emplacement() -> tuple[int| NaN, int| NaN]:
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

    return (
        find(variables_globales.curseur_pos_attendue_x, variables_globales.curseur_x, NAN),
        find(variables_globales.curseur_pos_attendue_y, variables_globales.curseur_y, NAN)
    )
