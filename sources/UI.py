from liste_boutons import *
from Attaque import Attaque, ATTAQUES_DISPONIBLES

def demander_pseudo(surface : Surface) -> Interruption:
    logging.debug(f"→ Interruption: demande du pseudo.")
    
    pseudo : str  = ""
    saisie : bool = True
    texte : Surface = Constantes.Polices.TITRE.render("Entrez votre pseudo :", True, NOIR)
    while saisie:
        Jeu.commencer_frame()
        
        pseudo, continuer = texte_entree_event(pseudo)
        if not continuer:
            break
        
        surface.fill(BLANC)
        blit_centre(surface, texte, (Jeu.pourcentage_largeur(50), Jeu.pourcentage_hauteur(45)))
        
        pseudo_affiche : Surface = Constantes.Polices.FOURRE_TOUT.render(pseudo, True, BLEU)
        blit_centre(surface, pseudo_affiche, (Jeu.pourcentage_largeur(50), Jeu.pourcentage_hauteur(50)))
        yield surface
    
    joueur.pseudo = pseudo
    logging.debug(f"← Fin interruption (demande du pseudo).")

def texte_entree_event(texte : str) -> tuple[str, bool]:
    continuer : bool = True

    TOUCHES_A_IGNORER : tuple[int, ...] = (
        pygame.K_LSHIFT, pygame.K_RSHIFT,
        pygame.K_LALT, pygame.K_RALT,
        pygame.K_LCTRL, pygame.K_CAPSLOCK,
        pygame.K_INSERT, pygame.K_AC_BACK,
        pygame.K_BREAK, pygame.K_CARET,
        pygame.K_END, 
        pygame.K_PAGEDOWN, pygame.K_PAGEUP,
        pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN,   # flemme de faire un système de curseur
        # on s'arrête ici pour l'instant
    )
    for event in pygame.event.get():
        verifier_pour_quitter(event)
        
        if event.type != pygame.KEYDOWN or event.key in TOUCHES_A_IGNORER:
            continue
        
        if event.key == pygame.K_RETURN and len(texte) > 0:
            continuer = False
            continue
        
        if event.key == pygame.K_BACKSPACE:
            texte = texte[:-1]  # on enlève le dernier caractère
            continue
        
        # On vérifie que la lettre soit correcte.
        lettre_ascii        : int = ord(event.unicode)
        est_lettre          : bool = 48  <= lettre_ascii <= 122 and not (58 <= lettre_ascii <= 62 or 92 <= lettre_ascii <= 96)  # nombre ou lettre latine (+ '?' et '@')
        est_lettre_speciale : bool = 192 <= lettre_ascii <= 255                                                                 # Lettre latine avec accent
        if len(texte) < 12 and (est_lettre or est_lettre_speciale or event.unicode in ('œ', '&', '!', ' ')):
            texte += event.unicode
            continue
        
    if texte == ' ':    # le nom ne peut pas être composé exclusivement d'espaces
        texte = ''
    if len(texte) >= 2 and texte[-2].isspace() and texte[-1].isspace(): # jamais deux caractères blancs à coté
        texte = texte[:-1]                                              # les espaces, nouvelles lignes, tabs...
    return (texte, continuer)

# TODO: J'aime pas le fait que ce soit hardcodé
# Il faudra changer ça avec l'ajout du système de cartes
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
    logging.debug(f"→ Interruption: affichage des informations d'une attaque.")
    
    texte_puissance   : Surface
    texte_vitesse     : Surface
    texte_description : Surface
    
    image : Surface = Surface((Jeu.largeur, Jeu.hauteur))
    
    image.fill(BLANC)
    
    attaque : Attaque = trouve_attaque_a_partir_du_curseur()
    texte_puissance   = Constantes.Polices.TITRE.render(f"Puissance: {attaque.puissance}", True, NOIR)
    texte_vitesse     = Constantes.Polices.TITRE.render(f"Vitesse: {attaque.vitesse}"    , True, NOIR)
    texte_description = Constantes.Polices.TITRE.render(attaque.desc                     , True, NOIR)
    
    blit_centre(image, texte_puissance  , (Jeu.pourcentage_largeur(33), Jeu.pourcentage_hauteur(50)))
    blit_centre(image, texte_vitesse    , (Jeu.pourcentage_largeur(66), Jeu.pourcentage_hauteur(50)))
    blit_centre(image, texte_description, (Jeu.pourcentage_largeur(50), Jeu.pourcentage_hauteur(57)))
    
    return image_vers_generateur(
        image,
        Duree(s=2),
        gerer_evenements=True,
        derniere_etape=lambda: logging.debug(f"← Fin interruption (infos d'une attaque).")
    )


def dessiner_boutons_attaques() -> None:
    for butt in boutons_attaques:
        butt.draw(Jeu.menus_surf)
    ButtonCursor.draw_cursors(Jeu.menus_surf)

def faux_chargement(surface : Surface, duree_totale : Duree = Duree(s=2.0)) -> Interruption:
    LONGUEUR_BARRE : int = 700
    ratio_barre : float = 0
    
    gradient : MultiGradient = MultiGradient([ROUGE, JAUNE, VERT])        # sinon ça donne un marron pas très estéthique
    while ratio_barre < 1:
        delta : Duree = Jeu.commencer_frame()
        verifier_pour_quitter()
        
        surface.fill(BLANC)
        dessiner_rect(
            surface,
            (Jeu.pourcentage_largeur(6.25), Jeu.pourcentage_hauteur(50)),
            (round(ratio_barre * LONGUEUR_BARRE), 50),
            
            couleur_remplissage=gradient.calculer_valeur(ratio_barre),
            epaisseur_trait=0
        )
        dessiner_rect(
            surface,
            (Jeu.pourcentage_largeur(6.25), Jeu.pourcentage_hauteur(50)),
            (LONGUEUR_BARRE, 50),
            couleur_bords=NOIR, dessiner_interieur=False,
            epaisseur_trait=5,
        )
        
        texte_chargement : Surface = Constantes.Polices.TITRE.render("Chargement...", True, NOIR)
        blit_centre(surface, texte_chargement, (Jeu.pourcentage_largeur(50), Jeu.pourcentage_hauteur(45)))
        
        ratio_barre += delta.secondes / duree_totale.secondes
        yield surface


def ecran_nombre_combat() -> Generator[Surface, None, None]:
    texte_combat : Surface = Constantes.Polices.TITRE.render(f"Combat n°{Jeu.num_etape}", True, NOIR)
    texte_shop   : Surface = Constantes.Polices.TITRE.render(f"Shop", True, NOIR)
    image : Surface = Surface(Jeu.fenetre.get_size())
    
    logging.info("")
    logging.info("")
    if Jeu.DECISION_SHOP(Jeu.num_etape):
        image.fill(CYAN)
        blit_centre(image, texte_shop, Jeu.centre_fenetre)
        
        logging.info(f"Entrée dans le shop de la zone {Jeu.num_etape}.")
    else:
        image.fill(BLANC)
        blit_centre(image, texte_combat, Jeu.centre_fenetre)
        
        logging.info(f"Début combat numéro {Jeu.num_etape}.")
    return image_vers_generateur(image, Duree(s=2), gerer_evenements=True)


def rafraichir_ecran(generateurs_dessin : list[Generator] = [], generateurs_UI : list[Generator] = [], to_send_dessin : Any = None, to_send_UI : Any = None) -> None:
    # Effacer l'écran en redessinant l'arrière-plan
    Jeu.fenetre.fill(BLANC)
    Jeu.menus_surf.fill(TRANSPARENT)
    
    # Dessiner le joueur
    joueur.dessiner(Jeu.fenetre)
    joueur.dessine_barre_de_vie(Jeu.fenetre, 500, 400)
    Jeu.menus_surf.blit(Constantes.Polices.TITRE.render(joueur.pseudo, True, NOIR), (499, 370))
    
    # Dessiner les monstres
    for monstre in Monstre.monstres_en_vie:
        monstre.dessiner(Jeu.fenetre, Jeu.pourcentage_largeur(70), Jeu.pourcentage_hauteur(15))  # ils sont tous à la même position pour l'instant
        monstre.dessiner_barre_de_vie(Jeu.fenetre, 50, 50)
        Jeu.menus_surf.blit(Constantes.Polices.TITRE.render(monstre.nom, True, NOIR), (49, 20))
    
    # Dessiner l'icône du toujours_crit
    if Attaque.toujours_crits:
        blit_centre(Jeu.fenetre, Attaque.CRIT_IMG, (Jeu.pourcentage_largeur(80), Jeu.pourcentage_hauteur(60)))
    
    # Dessiner le fond de l'interface
    pygame.draw.rect(Jeu.fenetre, NOIR, (0, Jeu.pourcentage_hauteur(75), 800, 600), 0)
    
    # Dessiner le curseur du menu de combat
    ButtonCursor.draw_cursors(Jeu.fenetre)
    
    # Dessiner le texte
    blit_centre(Jeu.fenetre, Constantes.Polices.TEXTE.render("ESPACE : utiliser", True, BLANC), (Jeu.pourcentage_largeur(85), Jeu.pourcentage_hauteur(81)))
    blit_centre(Jeu.fenetre, Constantes.Polices.TEXTE.render("I : info"         , True, BLANC), (Jeu.pourcentage_largeur(85), Jeu.pourcentage_hauteur(84)))
    
    # Dessin supplémentaire
    avancer_generateurs(generateurs_dessin, to_send_dessin)
    avancer_generateurs(generateurs_UI,     to_send_UI)
    
    # ...
    dessiner_boutons_attaques()
    
    # Mettre à jour l'affichage
    Jeu.display_flip()