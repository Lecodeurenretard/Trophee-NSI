from import_local import *
from Joueur       import Entite, Joueur, joueur
from Monstre      import Monstre
from Carte        import Attaque, Carte
from Item         import Item
from Bouton       import Button

def demander_pseudo(surface : Surface) -> Interruption:
    logging.debug(f"→ Interruption: demande du pseudo.")
    
    pseudo : str  = ""
    texte : Surface = Polices.TITRE.render("Entrez votre pseudo :", True, NOIR)
    while True:
        Jeu.commencer_frame()
        
        pseudo, continuer = texte_entree_event(pseudo)
        if not continuer and pseudo != '':
            break
        
        surface.fill(BLANC)
        blit_centre(surface, texte, Jeu.pourcentages_coordonees(50, 45, ret_pos=False))
        
        pseudo_affiche : Surface = Polices.FOURRE_TOUT.render(pseudo, True, BLEU)
        blit_centre(surface, pseudo_affiche, Jeu.centre_fenetre)
        yield surface
    
    joueur.nom = pseudo
    logging.debug(f"← Fin interruption (demande du pseudo).")

def texte_entree_event(texte : str) -> tuple[str, bool]:
    continuer : bool = True

    TOUCHES_A_IGNORER : tuple[int, ...] = (
        pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN,   # flemme de faire un système de curseur
        pygame.K_LSHIFT, pygame.K_RSHIFT,
        pygame.K_LALT, pygame.K_RALT,
        pygame.K_LCTRL, pygame.K_RCTRL,
        pygame.K_PAGEDOWN, pygame.K_PAGEUP,
        pygame.K_CAPSLOCK, pygame.K_END,
        pygame.K_INSERT, pygame.K_AC_BACK,
        pygame.K_BREAK, pygame.K_CARET,
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
        
    if texte.isspace():    # le nom ne peut pas être composé exclusivement de whitespaces
        texte = ''
    if len(texte) >= 2 and texte[-2].isspace() and texte[-1].isspace(): # jamais deux caractères blancs à coté
        texte = texte[:-1]                                              # les espaces, nouvelles lignes, tabs...
    return (texte, continuer)

# TODO: TOREMOVE
def trouve_carte_a_partir_du_curseur() -> Carte:
    raise AssertionError("Cette fonction est cassée, elle sera réparée sous peu.")
    
    # Ce qui est important, c'est que le bouton soit dans le groupe Attaques
    curseur_pos : Pos = Pos(0, 0)
    
    # Il faudra changer ça avec l'ajout du système de cartes
    if curseur_pos == Pos(0, 0):
        return Carte('Soin')
    
    if curseur_pos == Pos(1, 0):
        return Carte('Magie')
    
    if curseur_pos == Pos(0, 1):
        return Carte('Physique')
    
    if curseur_pos == Pos(1, 1):
        return Carte('Skip')
    
    raise RuntimeError(f"Le curseur est à une position innatendue: {curseur_pos}.")

def afficher_infos() -> Interruption:
    logging.debug(f"→ Interruption: affichage des informations d'une attaque.")
    
    texte_puissance   : Surface
    texte_description : Surface
    
    image : Surface = Surface((Jeu.largeur, Jeu.hauteur))
    
    image.fill(BLANC)
    
    carte : Carte = trouve_carte_a_partir_du_curseur()
    texte_puissance   = Polices.TITRE.render(f"Puissance: {carte.puissance}", True, NOIR)
    texte_description = Polices.TITRE.render(carte.description              , True, NOIR)
    
    blit_centre(image, texte_puissance  , Jeu.pourcentages_coordonees(50, 50, ret_pos=False))
    blit_centre(image, texte_description, Jeu.pourcentages_coordonees(50, 57, ret_pos=False))
    
    return image_vers_generateur(
        image,
        Duree(s=2),
        gerer_evenements=True,
        derniere_etape=lambda: logging.debug(f"← Fin interruption (infos d'une attaque).")
    )

def faux_chargement(surface : Surface, duree_totale : Duree = Duree(s=2.0)) -> Interruption:
    LONGUEUR_BARRE : int = 700
    ratio_barre : float = 0
    
    gradient : MultiGradient = MultiGradient([ROUGE, JAUNE, VERT])        # sinon ça donne un marron pas très estéthique
    while ratio_barre < 1:
        delta : Duree = Jeu.commencer_frame()
        verifier_pour_quitter()
        
        surface.fill(BLANC)
        # Le contour de la barre
        dessiner_rect(
            surface,
            Jeu.centre_fenetre,
            (round(ratio_barre * LONGUEUR_BARRE), 50),
            couleur_remplissage=gradient.calculer_valeur(ratio_barre),
            epaisseur_trait=0,
            centre_x=True,
        )
        # Ce qui va remplir la barre
        dessiner_rect(
            surface,
            Jeu.centre_fenetre,
            (LONGUEUR_BARRE, 50),
            couleur_bords=NOIR, dessiner_interieur=False,
            epaisseur_trait=5,
            centre_x=True,
        )
        
        texte_chargement : Surface = Polices.TITRE.render("Chargement...", True, NOIR)
        blit_centre(surface, texte_chargement, Jeu.pourcentages_coordonees(50, 45, ret_pos=False))
        
        ratio_barre += delta.secondes / duree_totale.secondes
        yield surface


def ecran_nombre_combat() -> Generator[Surface, None, None]:
    texte_combat : Surface = Polices.TITRE.render(f"Combat n°{Jeu.num_etape}", True, NOIR)
    texte_shop   : Surface = Polices.TITRE.render(f"Shop", True, NOIR)
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
    for i, entite in Entite.vivantes.items():
        dessiner_texte(
            surface,
            entite.decrire_stats(),
            rgb_to_rgba(GRIS_CLAIR, transparence=128),
            (
                Jeu.pourcentage_largeur(33) * i + 2,
                0,
                Jeu.pourcentage_largeur(33),
                Jeu.hauteur
            ),
            Polices.TEXTE,
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
        "vie maximum"        : joueur.stats_totales.vie_max         - Joueur.STATS_DE_BASE.vie_max,
        "force"              : joueur.stats_totales.force           - Joueur.STATS_DE_BASE.force,
        "défense"            : joueur.stats_totales.defense         - Joueur.STATS_DE_BASE.defense,
        "magie"              : joueur.stats_totales.magie           - Joueur.STATS_DE_BASE.magie,
        "défense magique"    : joueur.stats_totales.defense_magique - Joueur.STATS_DE_BASE.defense_magique,
        "puissance des crits": joueur.stats_totales.crit_puissance  - Joueur.STATS_DE_BASE.crit_puissance,
        "resitance aux crits": joueur.stats_totales.crit_resitance  - Joueur.STATS_DE_BASE.crit_resitance,
    }
    
    y = 0
    for stat, diff in differences.items():
        coul  = GRIS_CLAIR
        if diff < 0: coul = ROUGE
        if diff > 0: coul = VERT
        
        txt = Polices.TEXTE.render(f"{stat}: {int(diff):+d}", True, coul)
        surface.blit(txt, (10, y))
        y += txt.get_rect().height + 5

def dessiner_infos() -> None:
    """Si les bonnes touches sont pressées, dessine les infos."""
    if pygame.key.get_pressed()[Touches.DIFFS]:
        dessiner_diff_stats_joueur(Jeu.infos_surf)
    
    elif pygame.key.get_pressed()[Touches.DBG_INFOS_ENTITES] and bool(params.mode_debug):
        dessiner_descriptions_entites(Jeu.infos_surf)

def rafraichir_ecran(generateurs_dessin : list[Generator] = [], generateurs_UI : list[Generator] = [], to_send_dessin : Any = None, to_send_UI : Any = None) -> None:
    # Effacer l'écran en redessinant l'arrière-plan
    Jeu.fenetre.fill(BLANC)
    Jeu.menus_surf.fill(TRANSPARENT)
    
    # Dessiner les entités
    for entites in Entite.vivantes.values():
        entites.dessiner(Jeu.fenetre)
        entites.dessiner_UI(Jeu.fenetre)
    
    # Vérifie si les cartes doivent être dessinées
    montrer_cartes : bool = True
    for touche in Touches.DBG_CACHER_CARTES:
        if pygame.key.get_pressed()[touche]:
            montrer_cartes = False
            break
    
    if montrer_cartes or not bool(params.mode_debug):
        # Avance et dessine l'animation des cartes affichées
        a_cacher : list[int] = []
        liste_carte : list[tuple[int, Carte]]=  list(Carte.cartes_affichees.items())
        for i, carte in sorted(liste_carte, key=lambda t: t[1].pos_defaut.x):    # dessine les cartes dans l'ordre croissant des abscisses
            try:
                next(carte.animation_generateur)   # .items() garde les références donc tout va bien
            except StopIteration:
                a_cacher.append(i)
        
        # Nettoyage de Carte.cartes_affichees_anim[] (ici sinon on enlève des clefs)
        for index in a_cacher:
            Carte.cartes_affichees[index].cacher()
    
    # Dessiner l'icône du toujours_crit
    if Attaque.toujours_crits:
        blit_centre(Jeu.menus_surf, Carte.CRIT_IMG, Jeu.pourcentages_coordonees(80, 60, ret_pos=False))
    
    # Dessiner le nombre de coups restant
    dessiner_rect(
        Jeu.menus_surf,
        Jeu.pourcentages_coordonees(85, 87),
        Jeu.pourcentages_fenetre(20, 10, ret_vec=False),
        couleur_remplissage=GRIS_CLAIR,
        couleur_bords=BLANC,
        centre_x=True,
        centre_y=True,
        border_radius=3,
    )
    txt_coups = Polices.FOURRE_TOUT.render(
        f"{Jeu.attaques_restantes_joueur} coups restants",
        True,
        Gradient.calculer_valeur_s(
            CYAN,
            ROUGE,
            abs(Jeu.attaques_restantes_joueur) / Jeu.ATTAQUES_PAR_TOUR,
            sens_lecture=SensLecture.ARRIERE,   # le ratio décroit
        )
    )
    blit_centre(
        Jeu.menus_surf,
        txt_coups,
        Jeu.pourcentages_coordonees(85, 87, ret_pos=False),
    )
    
    # Dessin supplémentaire
    avancer_generateurs(generateurs_dessin, to_send_dessin)
    avancer_generateurs(generateurs_UI,     to_send_UI)
    
    # Si les bonnes touches sont appuyées, affiche les infos ou les diffs
    dessiner_infos()
    
    # Mettre à jour l'affichage
    Jeu.display_flip()



def dessiner_nombre_pieces(surface : Surface, boite_inventaire : Rect, ordonnees : int = Jeu.pourcentage_hauteur(5)) -> None:
    if params.argent_infini.case_cochee:
        dessiner_texte(
            surface,
            "genre, beaucoup de p",
            JAUNE_PIECE,
            (
                boite_inventaire.left + 10, ordonnees,
                boite_inventaire.width, ordonnees + Jeu.pourcentage_hauteur(5)
            ),
            Polices.TEXTE,
            True,
        )
    else:
        TEXTE_PIECES = Polices.TEXTE.render(
            f"{joueur.nb_pieces}p",
            True, JAUNE_PIECE,
        )
        surface.blit(TEXTE_PIECES, (
            boite_inventaire.left + boite_inventaire.width // 2,
            ordonnees,
        ))

def dessiner_inventaire(surface : Surface, boite_inventaire : Rect) -> None:
    y : int = Jeu.pourcentage_hauteur(9)     # début affichage items inventaire
    for item in joueur.inventaire:
        icone : Surface = pygame.transform.scale_by(
            item.sprite,
            (boite_inventaire.width - Jeu.pourcentage_hauteur(1)) / item.sprite.get_rect().width
        )
        
        surface.blit(
            icone,
            (boite_inventaire.left, y)
        )
        y += icone.get_bounding_rect().height + Jeu.pourcentage_hauteur(2)

def rafraichir_ecran_shop(items : list[Item], abscisses : tuple[int, ...], rect_inventaire : Rect, epaisseur_trait : int, bouton : Button, afficher_avertissements : bool = False) -> None:
    Jeu.fenetre.fill(BLANC)
    
    # Dessine l'inventaire du joueur
    dessiner_rect(
        Jeu.fenetre,
        rect_inventaire.topleft, rect_inventaire.size,
        couleur_remplissage=GRIS, couleur_bords=NOIR,
        epaisseur_trait=epaisseur_trait
    )
    
    # ...
    dessiner_nombre_pieces(Jeu.menus_surf, rect_inventaire)
    dessiner_inventaire(Jeu.fenetre, rect_inventaire)
    dessiner_infos()
    
    bouton.draw(Jeu.menus_surf, point_size=0)
    for item, pourcentage_abscisse in zip(items, abscisses):
        item.dessiner(Jeu.fenetre, pourcentage_abscisse, afficher_avertissements=afficher_avertissements)
    
    Jeu.display_flip()