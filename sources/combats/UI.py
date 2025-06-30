from fonctions_vrac import *
from Joueur import *
from Monstre import *
from Curseur import *

curseur_menu_combat : Curseur = Curseur(
    (50, 350),
    (13 * HAUTEUR // 16, 13 * HAUTEUR // 16 + 70)
)

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
    curseur_empl : tuple[int, int]= curseur_menu_combat.get_position_dans_position()
    
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
    dessiner_nom(joueur.get_pseudo(), Pos(499, 370))
    
    # Dessiner les monstres
    if len(Monstre.monstres_en_vie) != 0:   # TODO: S'il y en a plusieur, les décaler
        monstre_a_dessiner : Monstre = Monstre.monstres_en_vie[0]
        monstre_a_dessiner.dessiner(fenetre, 6 * LARGEUR // 10, HAUTEUR // 4 - 100)
        monstre_a_dessiner.dessiner_barre_de_vie(fenetre, 50, 50)
        dessiner_nom(monstre_a_dessiner.get_nom(), Pos(49, 20))
    
    # Dessiner le curseur du menu de combat
    curseur_menu_combat.dessiner(fenetre, VERT, 10)
    
    # Dessiner le texte
    fenetre.blit(TEXTE_INFO_UTILISER    , (620, (13 * HAUTEUR // 16) - 12))
    fenetre.blit(TEXTE_INFO_INFO        , (620, (13 * HAUTEUR // 16) + 20))
    
    dessiner_boutons_attaques()
    
    # Mettre à jour l'affichage
    pygame.display.flip()