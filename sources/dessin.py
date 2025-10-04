from import_var import *
from Pos        import Pos
from Duree      import Duree
from Jeu import verifier_pour_quitter

def dessiner_rect(
        surface : Surface,
        position : tuple[int, int]|Pos, dimensions : tuple[int, int]|list[int],
        couleur_remplissage : color = ROUGE, couleur_bords : color = NOIR,
        epaisseur_trait : int = 1, dessiner_interieur : bool = True,
        centre_x : bool = False, centre_y : bool = False,
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
            )
        )
    
    if epaisseur_trait > 0:
        pygame.draw.rect(
            surface,
            couleur_bords,
            (
                position.x, position.y,
                dimensions[0], dimensions[1]
            ),
            width=epaisseur_trait
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

def dessiner_nom(surface : Surface, nom : str, position : Pos) -> None:
    # c'est plus clair de mettre cette ligne en procédure
    surface.blit(Constantes.Polices.TITRE.render(nom, True, NOIR), tuple(position))

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
        except GeneratorExit:
            break
    
    if derniere_etape is not None:
        derniere_etape()