from import_var import *
from Jeu import verifier_pour_quitter
from fonctions_vrac import blit_centre

def dessiner_rect(
        surface : Surface,
        position : tuple[int, int]|Pos, dimensions : tuple[int, int]|list[int],
        couleur_remplissage : color = ROUGE, couleur_bords : color = NOIR,
        epaisseur_trait : int = 1, dessiner_interieur : bool = True,
        centre_x : bool = False, centre_y : bool = False,
        border_radius = -1,
        border_radius_tl = -1, border_radius_tr = -1,
        border_radius_bl = -1, border_radius_br = -1,
    ) -> None:
    if type(position) is tuple:
        position = Pos(position)
    assert(type(position) is Pos)   # c'est censé être sûr mais Pylance ne le pense pas
    
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

def dessiner_barre_de_vie(surface : Surface, pos_x : int, pos_y : int, ratio_vie : float, longueur_remplissage : int) -> None:
    from parametres_vars import mode_debug
    
    def dessin(remplissage : color) -> None:
        dessiner_rect(surface, (pos_x, pos_y), (longueur_remplissage, Constantes.UI_HAUTEUR_BARRE_DE_VIE), couleur_remplissage=remplissage, epaisseur_trait=0)
        dessiner_rect(surface, (pos_x, pos_y), (Constantes.UI_LONGUEUR_BARRE_DE_VIE, Constantes.UI_HAUTEUR_BARRE_DE_VIE), couleur_bords=NOIR, epaisseur_trait=2, dessiner_interieur=False)
        
    
    if mode_debug.case_cochee:
        dessin(GRIS)
        return
    
    couleur_remplissage : rgb = VERT
    if ratio_vie <= .2:
        couleur_remplissage = ROUGE
    elif ratio_vie <= .5:
        couleur_remplissage = JAUNE
    elif ratio_vie == 1:
        couleur_remplissage = CYAN
    
    dessin(couleur_remplissage)

def image_vers_generateur(
        image : Surface,
        temps_affichage : Duree,
        gerer_evenements : bool = False,
        derniere_etape : Optional[Callable[[], Any]] = None
    ) -> Generator[Surface, None, None]:    # C'est pas une iterruption donc pas besoin de la typer comme telle
    """
    Renvoie un générateur qui renvoie `image` pendant le temps requis.
    Le paramètre optionnel `derniere_etape()` est une fonction à être appelées à la dernière étape du générateur.
    Bien que `derniere_etape()` puisse retourner n'importe quoi, le résultat sera juste ignoré.
    """
    fin : Duree = Jeu.duree_execution + temps_affichage
    while Jeu.duree_execution < fin:
        if gerer_evenements:
            verifier_pour_quitter()
        try:
            yield image
        except (StopIteration, GeneratorExit):
            break
    
    if derniere_etape is not None:
        derniere_etape()

def dessiner_gif(surface : Surface, pattern : str, duree_affichage : Duree, pos : Pos|tuple[int, int], loop : bool = False, scale : bool = False) -> Generator[None, None, None]:
    """
    Renvoie un générateur qui dessine chaque image du dossier les unes à la suite des autres par ordre alphabétique sur `surface`, chacunes pendant `duree_affichage`. Pour savoir combien de temps s'est écoulé, la fonction utilise l'horloge interne.
    `pattern` est un pattern glob qui est passé sans filtre à `glob()`.
    Si `loop` est true, le générateur reprendra au début quand il atteint la fin.
    Si `scale` est true, les images serons redimensionnées pour remplir complètement `surface`.
    
    Si depuis le dernier appel il s'est écoulé plus de `duree_affichage`, le générateur ne fera que passer à la prochaine image peut importe le temps supplémentaire.
    """
    if type(pos) is Pos:
        pos = pos.tuple
    assert(type(pos) is tuple)
    
    
    images : list[str] = sorted(glob(pattern))
    if len(images) == 0:
        raise FileNotFoundError("Aucun fichier ne respecte le pattern. Vérifiez qu'il soit correct.")
    
    premiere_fois : bool = True
    while premiere_fois or loop:
        premiere_fois = False
        
        for image in images:
            img : Surface = pygame.image.load(image)
            if scale:
                img = pygame.transform.scale(img, surface.get_size())
            
            img_gen = image_vers_generateur(img, duree_affichage)
            while True:
                try:
                    blit_centre(surface, next(img_gen), pos)
                    yield
                except StopIteration:
                    break
                except GeneratorExit:
                    return