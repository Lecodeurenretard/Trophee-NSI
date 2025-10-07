from liste_boutons import *
from Monstre import *

def demander_pseudo() -> None:
    pseudo : str  = ""
    saisie : bool = True
    texte : Surface = Constantes.Polices.TITRE.render("Entrez votre pseudo :", True, NOIR)
    while saisie:
        Jeu.commencer_frame()
        
        pseudo, continuer = texte_entree_event(pseudo)
        if not continuer:
            break
        
        Jeu.fenetre.fill(BLANC)
        blit_centre(Jeu.fenetre, texte, (Jeu.pourcentage_largeur(50), Jeu.pourcentage_hauteur(45)))
        
        pseudo_affiche : Surface = Constantes.Polices.FOURRE_TOUT.render(pseudo, True, BLEU)
        blit_centre(Jeu.fenetre, pseudo_affiche, (Jeu.pourcentage_largeur(50), Jeu.pourcentage_hauteur(50)))
        
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
    logging.debug(f"→ Interruption: affichage des informations d'une attaque.")
    
    texte_puissance   : Surface
    texte_vitesse     : Surface
    texte_description : Surface
    
    image : Surface = Surface((Jeu.LARGEUR, Jeu.HAUTEUR))
    
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

def faux_chargement(duree_totale : Duree = Duree(s=2.0)) -> None:
    LONGUEUR_BARRE : int = 700
    ratio_barre : float = 0
    
    gradient : Gradient = Gradient(ROUGE, VERT)
    while ratio_barre < 1:
        delta : Duree = Jeu.commencer_frame()
        verifier_pour_quitter()
        
        Jeu.fenetre.fill(BLANC)
        dessiner_rect(
            Jeu.fenetre,
            (Jeu.pourcentage_largeur(6.25), Jeu.pourcentage_hauteur(50)),
            (round(ratio_barre * LONGUEUR_BARRE), 50),
            couleur_remplissage=gradient.calculer_valeur(
                ratio_barre,
                r=ecraser_easing(Easing.TRIGONOMETRIC, (.5, 1)),
                g=ecraser_easing(Easing.TRIGONOMETRIC, (0, .5)),
            ),
            epaisseur_trait=0
        )
        dessiner_rect(
            Jeu.fenetre,
            (Jeu.pourcentage_largeur(6.25), Jeu.pourcentage_hauteur(50)),
            (LONGUEUR_BARRE, 50),
            couleur_bords=NOIR, dessiner_interieur=False,
            epaisseur_trait=5,
        )
        
        texte_chargement : Surface = Constantes.Polices.TITRE.render("Chargement...", True, NOIR)
        blit_centre(Jeu.fenetre, texte_chargement, (Jeu.pourcentage_largeur(50), Jeu.pourcentage_hauteur(45)))
        
        pygame.display.flip()

        ratio_barre += delta.secondes / duree_totale.secondes


def ecran_nombre_combat() -> Generator[Surface, None, None]:
    texte_combat : Surface = Constantes.Polices.TITRE.render(f"Combat n°{Jeu.num_combat}", True, NOIR)
    
    image = Surface(Jeu.fenetre.get_size())
    image.fill(BLANC)
    blit_centre(image, texte_combat, Jeu.CENTRE_FENETRE)
    
    logging.info("")
    logging.info(f"Début combat numéro {Jeu.num_combat}")
    return image_vers_generateur(image, Duree(s=2), gerer_evenements=True)


def rafraichir_ecran(generateurs_dessin : list[Generator] = [], generateurs_UI : list[Generator] = []) -> None:
    # Effacer l'écran en redessinant l'arrière-plan
    Jeu.fenetre.fill(BLANC)
    Jeu.menus_surf.fill(TRANSPARENT)
    
    # Dessiner le joueur
    joueur.dessiner(Jeu.fenetre)
    joueur.dessine_barre_de_vie(Jeu.fenetre, 500, 400)
    dessiner_nom(Jeu.menus_surf, joueur.pseudo, Pos(499, 370))
    
    # Dessiner les monstres
    if len(Monstre.monstres_en_vie) != 0:
        for monstre in Monstre.monstres_en_vie:
            monstre.dessiner(Jeu.fenetre, Jeu.pourcentage_largeur(70), Jeu.pourcentage_hauteur(15))  # ils sont tous à la même position pour l'instant
            monstre.dessiner_barre_de_vie(Jeu.fenetre, 50, 50)
            dessiner_nom(Jeu.menus_surf, monstre.nom, Pos(49, 20))
    
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
    avancer_generateurs(generateurs_dessin)
    avancer_generateurs(generateurs_UI)
    
    # ...
    dessiner_boutons_attaques()
    
    # On oublie pas d'intégrer les menus
    Jeu.fenetre.blit(Jeu.menus_surf, (0, 0))
    
    # Mettre à jour l'affichage
    pygame.display.flip()