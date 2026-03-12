import os
from import_local import *
from Joueur       import Entite, Joueur, joueur
from Carte        import Attaque, Carte
from Item         import Item
from Bouton       import Bouton

def demander_pseudo() -> Interruption:
    logging.debug(f"→ Interruption: demande du pseudo.")
        
    pseudo : str  = ""
    texte : Surface = Fenetre.construire_police(Polices.TEXTE, 10).render("Entrez votre pseudo :", True, NOIR)
    while True:
        Jeu.commencer_frame()
        
        pseudo, continuer = texte_entree_event(pseudo)
        if not continuer and pseudo != '':
            break
        
        Fenetre.surface.fill(BLANC)
        blit_centre(0, texte, Fenetre.pourcentages_coordonnees(50, 45, ret_pos=False))
        
        pseudo_affiche : Surface = Fenetre.construire_police(Polices.FOURRE_TOUT, 12).render(pseudo, True, BLEU)
        blit_centre(0, pseudo_affiche, Fenetre.centre_fenetre)
        yield
    
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

def faux_chargement(duree_totale : Duree = Duree(s=2.0)) -> Interruption:
    LONGUEUR_BARRE : int = 700
    ratio_barre : float = 0
    
    gradient : MultiGradient = MultiGradient([ROUGE, JAUNE, VERT])        # sinon ça donne un marron pas très estéthique
    while ratio_barre < 1:
        delta : Duree = Jeu.commencer_frame()
        Fenetre.surface.fill(BLANC)
        
        # Le contour de la barre
        dessiner_rect(
            1,
            Fenetre.centre_fenetre,
            (round(ratio_barre * LONGUEUR_BARRE), 50),
            couleur_remplissage=gradient.calculer_valeur(ratio_barre),
            epaisseur_trait=0,
            centre_x=True,
        )
        # Ce qui va remplir la barre
        dessiner_rect(
            1,
            Fenetre.centre_fenetre,
            (LONGUEUR_BARRE, 50),
            couleur_bords=NOIR, dessiner_interieur=False,
            epaisseur_trait=5,
            centre_x=True,
        )
        
        texte_chargement : Surface = Fenetre.construire_police(Polices.TITRE, 11).render("Chargement...", True, NOIR)
        blit_centre(1, texte_chargement, Fenetre.pourcentages_coordonnees(50, 45, ret_pos=False))
        
        ratio_barre += delta.secondes / duree_totale.secondes
        yield


def ecran_nombre_combat(num_couche : int) -> Generator[None, None, None]:
    police_annonce = Fenetre.construire_police(Polices.TITRE, 9)
    texte_combat : Surface = police_annonce.render(f"Combat n°{Jeu.num_etape}", True, NOIR)
    texte_shop   : Surface = police_annonce.render(f"Shop", True, NOIR)
    image : Surface = Surface(Fenetre.surface.get_size())
    
    logging.info("")
    logging.info("")
    
    if Jeu.decision_shop(Jeu.num_etape):
        image.fill(CYAN)
        blit_centre(image, texte_shop, Fenetre.centre_fenetre)
        logging.info(f"Entrée dans le shop de la zone {Jeu.num_etape}.")
    else:
        image.fill(BLANC)
        blit_centre(image, texte_combat, Fenetre.centre_fenetre)
        logging.info(f"Début combat numéro {Jeu.num_etape}.")
        
    return blit_generateur(num_couche, image, Duree(s=2), gerer_evenements=True)


def dessiner_descriptions_entites(num_couche : int) -> None:
    """Dessine les infos quand on appuie sur F9."""
    for i, entite in Entite.vivantes.no_holes():
        dessiner_texte(
            num_couche,
            entite.decrire_stats(),
            rgb_to_rgba(GRIS_CLAIR, transparence=128),
            (
                Fenetre.pourcentage_largeur(33) * i + 2,
                0,
                Fenetre.pourcentage_largeur(33),
                Fenetre.hauteur
            ),
            Fenetre.construire_police(Polices.TEXTE, 7),
            aa=True,
            ecart_entre_lignes=5
        )
        pygame.draw.line(
            Fenetre.get_couche(num_couche),
            GRIS_CLAIR,
            (Fenetre.pourcentage_largeur(33) * i, 0),
            (Fenetre.pourcentage_largeur(33) * i, Fenetre.hauteur)
        )

def dessiner_diff_stats_joueur(num_couche : int) -> None:
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
        
        txt = Fenetre.construire_police(Polices.TEXTE, 7).render(f"{stat}: {int(diff):+d}", True, coul)
        Fenetre.get_couche(num_couche).blit(txt, (10, y))
        y += txt.get_rect().height + 5

def dessiner_infos() -> None:
    """Si les bonnes touches sont pressées, dessine les infos."""
    if pygame.key.get_pressed()[Touches.DIFFS]:
        dessiner_diff_stats_joueur(2)
    
    elif pygame.key.get_pressed()[Touches.DBG_INFOS_ENTITES] and bool(params.mode_debug):
        dessiner_descriptions_entites(2)

def rafraichir_ecran_combat() -> None:
    image_fond = pygame.image.load(f"{Chemins.IMG}etages/{Jeu.nom_etage()}.png")
    image_fond = pygame.transform.scale(image_fond, Fenetre.surface.get_size())
    
    # Afficher l'image de fond 
    Fenetre.surface.blit(image_fond, (0, 0))    # pas besoin de faire un .fill(), ça couvre déjà tout l'écran
    
    # Dessiner les entités
    for _, entites in Entite.vivantes.no_holes():
        entites.dessiner(0)
        entites.dessiner_UI(0)
    
    # Vérifie si les cartes doivent être dessinées
    dessiner_cartes : bool = True
    for touche in Touches.DBG_CACHER_CARTES:
        if bool(params.mode_debug) and pygame.key.get_pressed()[touche]:
            dessiner_cartes = False
            break
    
    if dessiner_cartes:
        # Avance et dessine l'animation des cartes affichées
        it_carte = (pair[1] for pair in Carte.cartes_affichees.no_holes())    # un itérateur sur les cartes
        for carte in Carte.ordre_dessin(it_carte):
            try:
                next(carte.animation_generateur)
            except StopIteration:
                ...
    
    # Dessiner l'icône du toujours_crit
    if Attaque.toujours_crits:
        blit_centre(1, Carte.CRIT_IMG, Fenetre.pourcentages_coordonnees(80, 60, ret_pos=False))
    
    # Dessiner le nombre de coups restant
    dessiner_rect(
        1,
        Fenetre.pourcentages_coordonnees(85, 87),
        Fenetre.pourcentages_fenetre(20, 10, ret_vec=False),
        couleur_remplissage=GRIS_CLAIR,
        couleur_bords=BLANC,
        centre_x=True,
        centre_y=True,
        border_radius=3,
    )
    txt_coups = Fenetre.construire_police(Polices.FOURRE_TOUT, 9).render(
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
        1,
        txt_coups,
        Fenetre.pourcentages_coordonnees(85, 87, ret_pos=False),
    )
    
    # Si les bonnes touches sont appuyées, affiche les infos ou les diffs
    dessiner_infos()
    
    # Mettre à jour l'affichage
    Fenetre.display_flip()



def dessiner_nombre_pieces(num_couche : int, boite_inventaire : Rect, ordonnees : int = Fenetre.pourcentage_hauteur(5)) -> None:
    if params.argent_infini.case_cochee:
        dessiner_texte(
            num_couche,
            "genre, beaucoup de p",
            JAUNE_PIECE,
            (
                boite_inventaire.left + 10, ordonnees,
                boite_inventaire.width, ordonnees + Fenetre.pourcentage_hauteur(5)
            ),
            Fenetre.construire_police(Polices.TEXTE, 5),
            True,
        )
    else:
        TEXTE_PIECES = Fenetre.construire_police(Polices.TEXTE, 8).render(
            f"{joueur.nb_pieces}p",
            True, JAUNE_PIECE,
        )
        Fenetre.blit_couche(
            num_couche,
            TEXTE_PIECES,
            (
                boite_inventaire.left + boite_inventaire.width // 2,
                ordonnees,
            )
        )

def dessiner_inventaire(surface : Surface, boite_inventaire : Rect) -> None:
    y : int = Fenetre.pourcentage_hauteur(9)     # début affichage items inventaire
    for item in joueur.inventaire:
        icone : Surface = pygame.transform.scale_by(
            item.sprite,
            (boite_inventaire.width - Fenetre.pourcentage_hauteur(1)) / item.sprite.get_rect().width
        )
        
        surface.blit(
            icone,
            (boite_inventaire.left, y)
        )
        y += icone.get_bounding_rect().height + Fenetre.pourcentage_hauteur(2)

def rafraichir_ecran_shop(items : list[Item], abscisses : tuple[int, ...], rect_inventaire : Rect, epaisseur_trait : int, bouton : Bouton, afficher_avertissements : bool = False) -> None:
    Fenetre.surface.fill(BLANC)
    
    # Dessine l'inventaire du joueur
    dessiner_rect(
        Fenetre.surface,
        rect_inventaire.topleft, rect_inventaire.size,
        couleur_remplissage=GRIS, couleur_bords=NOIR,
        epaisseur_trait=epaisseur_trait
    )
    
    # ...
    dessiner_nombre_pieces(1, rect_inventaire)
    dessiner_inventaire(Fenetre.surface, rect_inventaire)
    dessiner_infos()
    
    bouton.dessiner(1, point_size=0)
    for item, pourcentage_abscisse in zip(items, abscisses):
        item.dessiner(0, pourcentage_abscisse, afficher_avertissements=afficher_avertissements)
    
    Fenetre.display_flip()
