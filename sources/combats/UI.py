from liste_boutons import *
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
        blit_centre(fenetre, texte, (pourcentage_largeur(50), pourcentage_hauteur(45)))
        
        pseudo_affiche : Surface = globales.POLICE_FOURRE_TOUT.render(pseudo, True, BLEU)
        blit_centre(fenetre, pseudo_affiche, (pourcentage_largeur(50), pourcentage_hauteur(50)))
        
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

def afficher_info() -> Interruption:
    texte_puissance   : Surface
    texte_vitesse     : Surface
    texte_description : Surface
    
    image : Surface = Surface((LARGEUR, HAUTEUR))
    
    image.fill(BLANC)
    
    attaque : Attaque = trouve_attaque_a_partir_du_curseur()
    texte_puissance   = globales.POLICE_TITRE.render(f"Puissance: {attaque.puissance}", True, NOIR)
    texte_vitesse     = globales.POLICE_TITRE.render(f"Vitesse: {attaque.vitesse}", True, NOIR)
    texte_description = globales.POLICE_TITRE.render(attaque.desc, True, NOIR)
    
    blit_centre(image, texte_puissance  , (pourcentage_largeur(33), pourcentage_hauteur(50)))
    blit_centre(image, texte_vitesse    , (pourcentage_largeur(66), pourcentage_hauteur(50)))
    blit_centre(image, texte_description, (pourcentage_largeur(50), pourcentage_hauteur(57)))
    
    return image_vers_generateur(image, Duree(s=2))


def dessiner_boutons_attaques() -> None:
    for butt in boutons_attaques:
        butt.draw(menus_surf)
    ButtonCursor.draw_cursors(menus_surf)

def faux_chargement(duree : Duree = Duree(s=7.0)) -> None:
    barre : int = 0
    NB_ITERATION : int = 700
    while barre < NB_ITERATION:
        fenetre.fill(BLANC)
        
        pygame.draw.rect(fenetre, NOIR, (pourcentage_largeur(6.25), pourcentage_hauteur(50), barre, 50), 0)
        
        texte_chargement : Surface = globales.POLICE_TITRE.render("Chargement...", True, NOIR)
        blit_centre(fenetre, texte_chargement, (pourcentage_largeur(50), pourcentage_hauteur(45)))
        
        pygame.display.flip()
        
        barre += 2
        
        attendre = pause(duree // NB_ITERATION)    # On assume que toutes les actions de la boucle sont instantanées
        while next(attendre):
            commencer_frame()   # celle-ci ne l'est pas car clock.tick() peut prendre entre 0 et 16ms à exécuter

def ecran_nombre_combat() -> Generator[Surface, None, None]:
    texte_combat : Surface = globales.POLICE_TITRE.render(f"Combat n°{globales.nbr_combat}", True, NOIR)
    
    image = Surface(fenetre.get_size())
    image.fill(BLANC)
    blit_centre(image, texte_combat, CENTRE_FENETRE)
    
    logging.info("")
    logging.info(f"Début combat numéro {globales.nbr_combat}")
    return image_vers_generateur(image, Duree(s=2))


def rafraichir_ecran(generateurs_dessin : list[Generator] = [], generateurs_UI : list[Generator] = []) -> None:
    # Effacer l'écran en redessinant l'arrière-plan
    fenetre.fill(BLANC)
    menus_surf.fill(TRANSPARENT)
    
    # Dessiner le joueur
    joueur.dessiner(fenetre)
    joueur.dessine_barre_de_vie(fenetre, 500, 400)
    dessiner_nom(joueur.pseudo, Pos(499, 370))
    
    # Dessiner les monstres
    if len(Monstre.monstres_en_vie) != 0:
        for monstre in Monstre.monstres_en_vie:
            monstre.dessiner(fenetre, pourcentage_largeur(70), pourcentage_hauteur(15))  # ils sont tous à la même position pour l'instant
            monstre.dessiner_barre_de_vie(fenetre, 50, 50)
            dessiner_nom(monstre.nom, Pos(49, 20))
    
    # Dessiner l'icône du toujours_crit
    if Attaque.toujours_crits:
        blit_centre(fenetre, Attaque.CRIT_IMG, (pourcentage_largeur(80), pourcentage_hauteur(60)))
    
    # Dessiner le fond de l'interface
    pygame.draw.rect(fenetre, NOIR, (0, pourcentage_hauteur(75), 800, 600), 0)
    
    # Dessiner le curseur du menu de combat
    ButtonCursor.draw_cursors(fenetre)
    
    # Dessiner le texte
    blit_centre(fenetre, TEXTE_INFO_UTILISER, (pourcentage_largeur(85), pourcentage_hauteur(81)))
    blit_centre(fenetre, TEXTE_INFO_INFO    , (pourcentage_largeur(85), pourcentage_hauteur(84)))
    
    # Dessin supplémentaire
    avancer_generateurs(generateurs_dessin)
    avancer_generateurs(generateurs_UI)
    
    # ...
    dessiner_boutons_attaques()
    
    # On oublie pas d'intégrer les menus
    fenetre.blit(menus_surf, (0, 0))
    
    # Mettre à jour l'affichage
    pygame.display.flip()