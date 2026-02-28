from import_var import *
from Jeu import verifier_pour_quitter
from fonctions_vrac import blit_centre

def dessiner_rect(
        surface : Surface|int,
        pos : pos_t, dimensions : tuple[int, int]|list[int],
        couleur_remplissage : color = ROUGE, couleur_bords : color = ROUGE,
        epaisseur_trait : int = 1, dessiner_interieur : bool = True,
        centre_x : bool = False, centre_y : bool = False,
        border_radius = -1,
        border_radius_tl = -1, border_radius_tr = -1,
        border_radius_bl = -1, border_radius_br = -1,
    ) -> None:
    position = pos_t_vers_Pos(pos)
    if type(surface) is int:
        surface = Jeu.get_couche(surface)
    assert(type(surface) is Surface)
    
    if centre_x:
        position.x -= dimensions[0] // 2
    if centre_y:
        position.y -= dimensions[1] // 2
    
    if dessiner_interieur:
        pygame.draw.rect(
            surface,
            couleur_remplissage,
            (
                position.x, position.y,
                dimensions[0], dimensions[1]
            ),
            border_radius=border_radius,
            border_top_left_radius=border_radius_tl,
            border_top_right_radius=border_radius_tr,
            border_bottom_left_radius=border_radius_bl,
            border_bottom_right_radius=border_radius_br,
        )
    
    if epaisseur_trait > 0:
        pygame.draw.rect(
            surface,
            couleur_bords,
            (
                position.x, position.y,
                dimensions[0], dimensions[1]
            ),
            width=epaisseur_trait,
            border_radius=border_radius,
            border_top_left_radius=border_radius_tl,
            border_top_right_radius=border_radius_tr,
            border_bottom_left_radius=border_radius_bl,
            border_bottom_right_radius=border_radius_br,
        )

def blit_generateur(
        num_couche : int,
        image : Surface,
        temps_affichage : Duree,
        pos : pos_t = (0, 0),
        gerer_evenements : bool = False,
        derniere_etape : Optional[Callable[[], Any]] = None
    ) -> Generator[None, None, None]:    # Ce n'est pas une interruption donc pas besoin de la typer comme telle
    """
    Renvoie un générateur qui blit `image` sur la couche `num_couche` durant `temps_affichage`.
    Le paramètre optionnel `derniere_etape()` est une fonction à être appelées à la dernière étape du générateur.
    Bien que `derniere_etape()` puisse retourner n'importe quoi, le résultat sera juste ignoré.
    """
    fin : Duree = Jeu.duree_execution + temps_affichage
    while Jeu.duree_execution < fin:
        if gerer_evenements:
            verifier_pour_quitter()
        try:
            Jeu.blit_couche(num_couche, image, pos_t_vers_tuple(pos))
            yield
        except GeneratorExit:
            break
    
    if derniere_etape is not None:
        derniere_etape()

def dessiner_gif(num_couche : int, pattern : str, duree_affichage : Duree, pos : pos_t, en_boucle : bool = False, etendre : bool = False) -> Generator[None, None, None]:
    """
    Renvoie un générateur qui dessine chaque image du dossier les unes à la suite des autres par ordre alphabétique sur `surface`, chacunes pendant `duree_affichage`. Pour savoir combien de temps s'est écoulé, la fonction utilise l'horloge interne.
    `pattern` est un pattern glob qui est passé sans filtre à `glob()`.
    Si `en_boucle` est true, le générateur reprendra au début quand il atteint la fin.
    Si `etendre` est true, les images serons redimensionnées pour remplir complètement la couche.
    
    Si depuis le dernier appel il s'est écoulé plus de `duree_affichage`, le générateur ne fera que passer à la prochaine image peut importe le temps supplémentaire.
    """
    images : list[str] = sorted(glob(pattern))
    if len(images) == 0:
        raise FileNotFoundError("Aucun fichier ne respecte le pattern. Vérifiez qu'il soit correct.")
    
    premiere_fois : bool = True
    while premiere_fois or en_boucle:
        premiere_fois = False
        
        for image_chemin in images:
            img : Surface = pygame.image.load(image_chemin)
            if etendre:
                img = pygame.transform.scale(img, (Jeu.largeur, Jeu.hauteur))
            
            img_gen = blit_generateur(num_couche, img, duree_affichage, pos=pos)
            while True:
                try:
                    next(img_gen)
                    yield
                except StopIteration:
                    break
                except GeneratorExit:
                    return