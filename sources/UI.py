from liste_boutons import *
from Monstre import *

def demander_pseudo() -> None:
    pseudo : str  = ""
    saisie : bool = True
    texte : Surface = Constantes.Polices.TITRE.render("Entrez votre pseudo :", True, Constantes.NOIR)
    while saisie:
        pseudo, continuer = texte_entree_event(pseudo)
        if not continuer:
            break
        
        Jeu.fenetre.fill(Constantes.BLANC)
        blit_centre(Jeu.fenetre, texte, (pourcentage_largeur(50), pourcentage_hauteur(45)))
        
        pseudo_affiche : Surface = Constantes.Polices.FOURRE_TOUT.render(pseudo, True, Constantes.BLEU)
        blit_centre(Jeu.fenetre, pseudo_affiche, (pourcentage_largeur(50), pourcentage_hauteur(50)))
        
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
    
    image : Surface = Surface((Jeu.LARGEUR, Jeu.HAUTEUR))
    
    image.fill(Constantes.BLANC)
    
    attaque : Attaque = trouve_attaque_a_partir_du_curseur()
    texte_puissance   = Constantes.Polices.TITRE.render(f"Puissance: {attaque.puissance}", True, Constantes.NOIR)
    texte_vitesse     = Constantes.Polices.TITRE.render(f"Vitesse: {attaque.vitesse}"    , True, Constantes.NOIR)
    texte_description = Constantes.Polices.TITRE.render(attaque.desc                     , True, Constantes.NOIR)
    
    blit_centre(image, texte_puissance  , (pourcentage_largeur(33), pourcentage_hauteur(50)))
    blit_centre(image, texte_vitesse    , (pourcentage_largeur(66), pourcentage_hauteur(50)))
    blit_centre(image, texte_description, (pourcentage_largeur(50), pourcentage_hauteur(57)))
    
    return image_vers_generateur(image, Duree(s=2))


def dessiner_boutons_attaques() -> None:
    for butt in boutons_attaques:
        butt.draw(Jeu.menus_surf)
    ButtonCursor.draw_cursors(Jeu.menus_surf)

def faux_chargement(duree : Duree = Duree(s=7.0)) -> None:
    barre : int = 0
    NB_ITERATION : int = 700
    while barre < NB_ITERATION:
        Jeu.fenetre.fill(Constantes.BLANC)
        
        pygame.draw.rect(Jeu.fenetre, Constantes.NOIR, (pourcentage_largeur(6.25), pourcentage_hauteur(50), barre, 50), 0)
        
        texte_chargement : Surface = Constantes.Polices.TITRE.render("Chargement...", True, Constantes.NOIR)
        blit_centre(Jeu.fenetre, texte_chargement, (pourcentage_largeur(50), pourcentage_hauteur(45)))
        
        pygame.display.flip()
        
        barre += 2
        
        attendre = pause(duree // NB_ITERATION)    # On assume que toutes les actions de la boucle sont instantanées
        while not next(attendre):
            Jeu.commencer_frame()   # celle-ci ne l'est pas car clock.tick() peut prendre entre 0 et 16ms à exécuter

def ecran_nombre_combat() -> Generator[Surface, None, None]:
    texte_combat : Surface = Constantes.Polices.TITRE.render(f"Combat n°{Jeu.num_combat}", True, Constantes.NOIR)
    
    image = Surface(Jeu.fenetre.get_size())
    image.fill(Constantes.BLANC)
    blit_centre(image, texte_combat, Jeu.CENTRE_FENETRE)
    
    logging.info("")
    logging.info(f"Début combat numéro {Jeu.num_combat}")
    return image_vers_generateur(image, Duree(s=2))


def rafraichir_ecran(generateurs_dessin : list[Generator] = [], generateurs_UI : list[Generator] = []) -> None:
    # Effacer l'écran en redessinant l'arrière-plan
    Jeu.fenetre.fill(Constantes.BLANC)
    Jeu.menus_surf.fill(Constantes.TRANSPARENT)
    
    # Dessiner le joueur
    joueur.dessiner(Jeu.fenetre)
    joueur.dessine_barre_de_vie(Jeu.fenetre, 500, 400)
    dessiner_nom(joueur.pseudo, Pos(499, 370))
    
    # Dessiner les monstres
    if len(Monstre.monstres_en_vie) != 0:
        for monstre in Monstre.monstres_en_vie:
            monstre.dessiner(Jeu.fenetre, pourcentage_largeur(70), pourcentage_hauteur(15))  # ils sont tous à la même position pour l'instant
            monstre.dessiner_barre_de_vie(Jeu.fenetre, 50, 50)
            dessiner_nom(monstre.nom, Pos(49, 20))
    
    # Dessiner l'icône du toujours_crit
    if Attaque.toujours_crits:
        blit_centre(Jeu.fenetre, Attaque.CRIT_IMG, (pourcentage_largeur(80), pourcentage_hauteur(60)))
    
    # Dessiner le fond de l'interface
    pygame.draw.rect(Jeu.fenetre, Constantes.NOIR, (0, pourcentage_hauteur(75), 800, 600), 0)
    
    # Dessiner le curseur du menu de combat
    ButtonCursor.draw_cursors(Jeu.fenetre)
    
    # Dessiner le texte
    blit_centre(Jeu.fenetre, Constantes.Polices.TEXTE.render("ESPACE : utiliser", True, Constantes.BLANC), (pourcentage_largeur(85), pourcentage_hauteur(81)))
    blit_centre(Jeu.fenetre, Constantes.Polices.TEXTE.render("I : info"         , True, Constantes.BLANC), (pourcentage_largeur(85), pourcentage_hauteur(84)))
    
    # Dessin supplémentaire
    avancer_generateurs(generateurs_dessin)
    avancer_generateurs(generateurs_UI)
    
    # ...
    dessiner_boutons_attaques()
    
    # On oublie pas d'intégrer les menus
    Jeu.fenetre.blit(Jeu.menus_surf, (0, 0))
    
    # Mettre à jour l'affichage
    pygame.display.flip()