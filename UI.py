from fonctions_vrac import *
from Joueur import *
from Monstre import *

def demander_pseudo() -> None:
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
    
    joueur.set_pseudo(pseudo)

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

def trouve_attaque_a_partir_du_curseur() -> Attaque:
    curseur_empl : tuple[int|NaN, int|NaN]= get_curseur_emplacement()
    if isnan(curseur_empl[0]) or isnan(curseur_empl[1]):
        print(f"Position du curseur: {(variables_globales.curseur_x, variables_globales.curseur_y)}")
        raise ValueError("Le curseur n'est pas à un emplacement autorisé.")
    
    if curseur_empl == (0, 0):
        return ATTAQUES_DISPONIBLES['heal']
    
    if curseur_empl == (1, 0):
        return ATTAQUES_DISPONIBLES['magie']
    
    if curseur_empl == (0, 1):
        return ATTAQUES_DISPONIBLES['physique']
    
    if curseur_empl == (1, 1):
        return ATTAQUES_DISPONIBLES['skip']
    
    raise NotImplementedError("Il y a au moins un cas non pris en charge dans trouve_attaque_a_partir_du_curseur().")

def afficher_info() -> None:
    texte_info1 : pygame.Surface
    texte_info2 : pygame.Surface
    
    fenetre.fill(BLANC)
    
    attaque : Attaque = trouve_attaque_a_partir_du_curseur()
    texte_info1 = variables_globales.POLICE_GRAND.render(f"Puissance: {attaque.get_puissance()}", True, NOIR)
    texte_info2 = variables_globales.POLICE_GRAND.render(attaque.get_desc(), True, NOIR)
    
    fenetre.blit(texte_info1, (3 * LARGEUR // 10      , HAUTEUR // 2))
    fenetre.blit(texte_info2, (3 * LARGEUR // 10 - 100, HAUTEUR // 2 + 30))
    
    pygame.display.flip()
    time.sleep(2)



def dessiner_boutons_attaques() -> None:
    # Dessiner les boites
    pygame.draw.rect(fenetre, BLANC, (70 , (13 * HAUTEUR // 16) - 25, 200, 50), 5) # soin
    pygame.draw.rect(fenetre, BLANC, (70 , (13 * HAUTEUR // 16) + 45, 200, 50), 5) # torgnole
    pygame.draw.rect(fenetre, BLANC, (375, (13 * HAUTEUR // 16) - 25, 200, 50), 5) #...
    pygame.draw.rect(fenetre, BLANC, (375, (13 * HAUTEUR // 16) + 45, 200, 50), 5)
    
    # Dessiner les noms
    fenetre.blit(joueur.get_attaque_surface("heal")    , (140, (13 * HAUTEUR // 16) - 12))
    fenetre.blit(joueur.get_attaque_surface("physique"), (120, (13 * HAUTEUR // 16) + 60))
    fenetre.blit(joueur.get_attaque_surface("magie")   , (400, (13 * HAUTEUR // 16) - 12))
    fenetre.blit(joueur.get_attaque_surface("skip")    , (400, (13 * HAUTEUR // 16) + 60))


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
    
    # Dessiner le joueur
    joueur.dessiner(fenetre)
    joueur.dessine_barre_de_vie(fenetre, 500, 400)
    dessiner_nom(joueur.get_pseudo(), (499, 370))
    
    # Dessiner les monstres
    if len(Monstre.monstres_en_vie) != 0:
        monstre_a_dessiner : Monstre = Monstre.monstres_en_vie[0]
        monstre_a_dessiner.dessiner(fenetre, 6 * LARGEUR // 10, HAUTEUR // 4 - 100)
        monstre_a_dessiner.dessiner_barre_de_vie(fenetre, 50, 50)
        dessiner_nom(monstre_a_dessiner.get_nom(), (49, 20))
    
    # Dessiner le cercle à la nouvelle position
    pygame.draw.circle(fenetre, VERT, (variables_globales.curseur_x, variables_globales.curseur_y), 10, 0)
    
    # Dessiner le texte
    fenetre.blit(TEXTE_INFO_UTILISER    , (620, (13 * HAUTEUR // 16) - 12))
    fenetre.blit(TEXTE_INFO_INFO        , (620, (13 * HAUTEUR // 16) + 20))
    
    dessiner_boutons_attaques()
    
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
