from liste_boutons import *
from Attaque import Attaque

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
        blit_centre(surface, texte, Jeu.pourcentages_coordonees(50, 45))
        
        pseudo_affiche : Surface = Constantes.Polices.FOURRE_TOUT.render(pseudo, True, BLEU)
        blit_centre(surface, pseudo_affiche, Jeu.centre_fenetre)
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

def trouve_attaque_a_partir_du_curseur() -> Attaque:
    # Ce qui est important, c'est que le bouton soit dans le groupe Attaques
    curseur_pos : Pos = boutons_attaques[0].cursor.position_dans_positions
    
    # TODO: J'aime pas le fait que ce soit hardcodé
    # Il faudra changer ça avec l'ajout du système de cartes
    if curseur_pos == Pos(0, 0):
        return Attaque.avec_nom('Soin')
    
    if curseur_pos == Pos(1, 0):
        return Attaque.avec_nom('Magie')
    
    if curseur_pos == Pos(0, 1):
        return Attaque.avec_nom('Physique')
    
    if curseur_pos == Pos(1, 1):
        return Attaque.avec_nom('Skip')
    
    raise RuntimeError(f"Le curseur est à une position innatendue: {curseur_pos}.")

def afficher_infos() -> Interruption:
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
    
    blit_centre(image, texte_puissance  , Jeu.pourcentages_coordonees(33, 50))
    blit_centre(image, texte_vitesse    , Jeu.pourcentages_coordonees(66, 50))
    blit_centre(image, texte_description, Jeu.pourcentages_coordonees(50, 57))
    
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
            Jeu.pourcentages_coordonees(6.25, 50),
            (round(ratio_barre * LONGUEUR_BARRE), 50),
            
            couleur_remplissage=gradient.calculer_valeur(ratio_barre),
            epaisseur_trait=0
        )
        dessiner_rect(
            surface,
            Jeu.pourcentages_coordonees(6.25, 50),
            (LONGUEUR_BARRE, 50),
            couleur_bords=NOIR, dessiner_interieur=False,
            epaisseur_trait=5,
        )
        
        texte_chargement : Surface = Constantes.Polices.TITRE.render("Chargement...", True, NOIR)
        blit_centre(surface, texte_chargement, Jeu.pourcentages_coordonees(50, 45))
        
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


def dessiner_descriptions_entites(surface : Surface) -> None:
    """Dessine les infos quand on appuie sur F9."""
    for i, entite in enumerate(globales.entites_vivantes):
        dessiner_texte(
            surface,
            entite.decrire(),
            rgb_to_rgba(GRIS_CLAIR, transparence=128),
            (
                Jeu.pourcentage_largeur(33) * i + 2,
                0,
                Jeu.pourcentage_largeur(33),
                Jeu.hauteur
            ),
            Constantes.Polices.TEXTE,
            aa=True,
            ecart_entre_lignes=5
        )
        pygame.draw.line(
            surface,
            GRIS_CLAIR,
            (Jeu.pourcentage_largeur(33) * i, 0),
            (Jeu.pourcentage_largeur(33) * i, Jeu.hauteur)
        )

def dessiner_diff_stats_joueur(surface : Surface) -> None:
    """Dessine les gains/pertes par rapport aux stats de bases."""
    differences : dict[str, float] = {
        "vie maximum"        : joueur.stats.vie_max        - Joueur.STATS_DE_BASE.vie_max,
        "force"              : joueur.stats.force          - Joueur.STATS_DE_BASE.force,
        "défense"            : joueur.stats.defense        - Joueur.STATS_DE_BASE.defense,
        "magie"              : joueur.stats.magie          - Joueur.STATS_DE_BASE.magie,
        "défense magique"   : joueur.stats.defense_magique - Joueur.STATS_DE_BASE.defense_magique,
        "vitesse"            : joueur.stats.vitesse        - Joueur.STATS_DE_BASE.vitesse,
        "puissance des crits": joueur.stats.crit_puissance - Joueur.STATS_DE_BASE.crit_puissance,
        "resitance aux crits": joueur.stats.crit_resitance - Joueur.STATS_DE_BASE.crit_resitance,
    }
    
    y = 0
    for stat, diff in differences.items():
        coul  = GRIS_CLAIR
        if diff < 0: coul = ROUGE
        if diff > 0: coul = VERT
        
        txt = Constantes.Polices.TEXTE.render(f"{stat}: {int(diff):+d}", True, coul)
        surface.blit(txt, (10, y))
        y += txt.get_rect().height + 5

def dessiner_infos() -> None:
    """Dessine les infos Si les bonnes touches sont pressées."""
    if pygame.key.get_pressed()[Constantes.Touches.DIFFS]:
        dessiner_diff_stats_joueur(Jeu.infos_surf)
    
    elif pygame.key.get_pressed()[Constantes.Touches.DBG_INFOS_ENTITES] and bool(params.mode_debug):
        dessiner_descriptions_entites(Jeu.infos_surf)

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
        monstre.dessiner(Jeu.fenetre, *Jeu.pourcentages_coordonees(70, 15))  # ils sont tous à la même position pour l'instant
        monstre.dessiner_barre_de_vie(Jeu.fenetre, 50, 50)
        Jeu.menus_surf.blit(Constantes.Polices.TITRE.render(monstre.nom, True, NOIR), (49, 20))
    
    # Dessiner l'icône du toujours_crit
    if Attaque.toujours_crits:
        blit_centre(Jeu.menus_surf, Attaque.CRIT_IMG, Jeu.pourcentages_coordonees(80, 60))
    
    # Dessiner le fond de l'interface
    pygame.draw.rect(Jeu.fenetre, NOIR, (0, Jeu.pourcentage_hauteur(75), 800, 600), 0)
    
    # Dessiner le curseur du menu de combat
    ButtonCursor.draw_cursors(Jeu.menus_surf)
    
    # Dessiner le nombre de coups restant
    dessiner_rect(
        Jeu.menus_surf,
        Jeu.pourcentages_coordonees(85, 87),
        (150, 50),
        couleur_remplissage=GRIS_CLAIR,
        couleur_bords=BLANC,
        centre_x=True,
        centre_y=True,
        border_radius=3,
    )
    txt_coups = Constantes.Polices.FOURRE_TOUT.render(
        f"{abs(Jeu.attaques_restantes_joueur)}",
        True,
        Constantes.Couleurs.ROUGE
    )
    blit_centre(
        Jeu.menus_surf,
        txt_coups,
        Jeu.pourcentages_coordonees(85, 87),
    )
    
    # Dessiner le texte
    blit_centre(Jeu.fenetre, Constantes.Polices.TEXTE.render("ESPACE : utiliser", True, BLANC), Jeu.pourcentages_coordonees(85, 81))
    blit_centre(Jeu.fenetre, Constantes.Polices.TEXTE.render("I : info"         , True, BLANC), Jeu.pourcentages_coordonees(85, 84))
    
    # Dessin supplémentaire
    avancer_generateurs(generateurs_dessin, to_send_dessin)
    avancer_generateurs(generateurs_UI,     to_send_UI)
    
    # ...
    dessiner_boutons_attaques()
    
    # Si les bonnes touches sont appuyées, affiche les infos ou les diffs
    dessiner_infos()
    
    # Mettre à jour l'affichage
    Jeu.display_flip()