from liste_boutons import boutons_attaques, ButtonCursor
from Monstre import *

def demander_pseudo() -> None:
    pseudo : str  = ""
    saisie : bool = True
    texte : Surface = globales.POLICE_TITRE.render("Entrez votre pseudo :", True, NOIR)
    while saisie:
        pseudo, continuer = texte_entree_event(pseudo)
        if not continuer:
            break

        fenetre.fill(BLANC)
        fenetre.blit(texte, (LARGEUR // 2 - 180, HAUTEUR // 2 - 60))
        
        pseudo_affiche : Surface = globales.POLICE_TITRE.render(pseudo, True, BLEU)
        fenetre.blit(pseudo_affiche, (LARGEUR // 2 - 100, HAUTEUR // 2))
        
        pygame.display.flip()
    
    joueur.pseudo = pseudo

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
    curseur_pos : Pos = boutons_attaques[0].cursor.position_dans_positions   # Ce qui est important, c'est que le bouton soit dans le groupe Attaques
    
    if curseur_pos == Pos(0, 0):
        return ATTAQUES_DISPONIBLES['heal']
    
    if curseur_pos == Pos(1, 0):
        return ATTAQUES_DISPONIBLES['magie']
    
    if curseur_pos == Pos(0, 1):
        return ATTAQUES_DISPONIBLES['physique']
    
    if curseur_pos == Pos(1, 1):
        return ATTAQUES_DISPONIBLES['skip']
    
    raise ValueError("Il y a au moins un cas non pris en charge dans trouve_attaque_a_partir_du_curseur().")

def afficher_info() -> None:
    texte_info1 : Surface
    texte_info2 : Surface
    
    fenetre.fill(BLANC)
    
    attaque : Attaque = trouve_attaque_a_partir_du_curseur()
    texte_info1 = globales.POLICE_TITRE.render(f"Puissance: {attaque.puissance}", True, NOIR)
    texte_info2 = globales.POLICE_TITRE.render(attaque.desc, True, NOIR)
    
    fenetre.blit(texte_info1, (3 * LARGEUR // 10      , HAUTEUR // 2))
    fenetre.blit(texte_info2, (3 * LARGEUR // 10 - 100, HAUTEUR // 2 + 30))
    
    pygame.display.flip()
    attendre(2)


def dessiner_boutons_attaques() -> None:
    for butt in boutons_attaques:
        butt.draw(fenetre)
    ButtonCursor.draw_cursors(fenetre)

def chargement(duree : float = 7.0) -> None:
    barre : int = 0
    NB_ITERATION : int = 700
    while barre < NB_ITERATION:
        fenetre.fill(BLANC)
        
        pygame.draw.rect(fenetre, NOIR, (50, 300, barre, 50), 0)
        
        texte_chargement : Surface = globales.POLICE_TITRE.render("Chargement...", True, NOIR)
        fenetre.blit(texte_chargement, (300, 350))
        pygame.display.flip()
        
        barre += 2
        attendre(duree / NB_ITERATION)    # On assume que toutes les actions de la boucle sont instantanées

def afficher_nombre_combat(nbr_combat : int) -> None:
    texte_combat : Surface = globales.POLICE_TITRE.render(f"Combat n°{nbr_combat}", True, NOIR)
    
    fenetre.fill(BLANC)
    fenetre.blit(texte_combat, (LARGEUR // 2 - 100, HAUTEUR // 2 - 20))
    
    logging.info(f"")
    logging.info(f"Début combat numéro {nbr_combat}")
    pygame.display.flip()
    attendre(2)


def rafraichir_ecran() -> None:
    # Effacer l'écran en redessinant l'arrière-plan
    fenetre.fill(BLANC)
    
    # Dessiner le joueur
    joueur.dessiner(fenetre)
    joueur.dessine_barre_de_vie(fenetre, 500, 400)
    dessiner_nom(joueur.pseudo, Pos(499, 370))
    
    # Dessiner les monstres
    if len(Monstre.monstres_en_vie) != 0:   # TODO: S'il y en a plusieur, les décaler
        for monstre in Monstre.monstres_en_vie:
            monstre.dessiner(fenetre, 6 * LARGEUR // 10, HAUTEUR // 4 - 100)
            monstre.dessiner_barre_de_vie(fenetre, 50, 50)
            dessiner_nom(monstre.nom, Pos(49, 20))
    
    # Dessiner l'icône dutoujours_crit
    if Attaque.toujours_crits:
        fenetre.blit(Attaque.CRIT_IMG, (pourcentage_largeur(80), pourcentage_hauteur(60)))
    
    # Dessiner le fond de l'interface
    pygame.draw.rect(fenetre, NOIR, (0, 3 * HAUTEUR // 4, 800, 600), 0)
    
    # Dessiner le curseur du menu de combat
    ButtonCursor.draw_cursors(fenetre)
    
    # Dessiner le texte
    fenetre.blit(TEXTE_INFO_UTILISER, (620, (13 * HAUTEUR // 16) - 12))
    fenetre.blit(TEXTE_INFO_INFO    , (620, (13 * HAUTEUR // 16) + 20))
    
    # ...
    dessiner_boutons_attaques()
    
    # Calcul et affichage des FPS
    if globales.UI_autoriser_affichage_fps:
        framerate : str = "inf"
        if globales.delta != 0:
            framerate = str(round(1 / globales.delta))
        
        fenetre.blit(
            POLICE_TEXTE.render(framerate, True, NOIR),
            (pourcentage_largeur(95), pourcentage_hauteur(2))
        )
    
    # Mettre à jour l'affichage
    pygame.display.flip()