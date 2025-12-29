from UI           import *
from import_local import *
from Bouton       import Button


def _rafraichir_donnees() -> None:
    from Carte  import Carte
    from Item    import Item
    from Monstre import MonstreJSON
    
    logging.debug("Actualisation des cartes...")
    Carte.actualiser_donnees()
    
    logging.debug("Actualisation des items...")
    Item.actualiser_items()
    
    logging.debug("Actualisation des monstres...")
    MonstreJSON.actualiser_donnees()
    
    logging.debug("fini!")


def _evenements_parametres(bouton_sortie : Button, bouton_actualiser : Button) -> bool:
    """la boucle des évènements de `menu_paramètre()`. Renvoie si l'interruption s'arrête."""
    for ev in pygame.event.get():
        verifier_pour_quitter(ev)
        
        for parametre in PARAMETRES_NORMAUX:
            parametre.prendre_input(ev)
        
        if params.mode_debug.case_cochee:
            for parametre in PARAMETRES_TRICHE:
                parametre.prendre_input(ev)
        
        
        if ev.type == pygame.KEYDOWN and ev.key == Touches.SETTINGS:
            return True
        
        if ev.type != pygame.MOUSEBUTTONDOWN:
            continue
        
        if bool(params.mode_debug):
            bouton_actualiser.check_click(ev.pos)
        
        if bouton_sortie.check_click(ev.pos):
            return True
    return False

def menu_parametres() -> Interruption:
    logging.debug("→ Interruption: Paramètres")
    
    bouton_sortir : Button = Button(
        (
            *Jeu.pourcentages_coordonees(2, 2, ret_pos=False),
            Jeu.pourcentage_largeur(4), Jeu.pourcentage_largeur(4),
        ),
        img=f"{Chemins.IMG}/croix.png"
    )
    pos_dim_bouton_actualisation = (
        *Jeu.pourcentages_coordonees(50, 50, ret_pos=False),
        *Jeu.pourcentages_fenetre(30, 7, ret_vec=False),
    )
    butt_actualisation = Button(pos_dim_bouton_actualisation, "actualiser données", action=_rafraichir_donnees)
    
    
    TITRE_PARAMS : Surface = Polices.TITRE.render("Options de jeu"   , True, NOIR)
    TITRE_TRICHE : Surface = Polices.TITRE.render("Options de triche", True, NOIR)
    
    while True:
        if _evenements_parametres(bouton_sortir, butt_actualisation):
            break
        
        image : Surface = Surface((Jeu.largeur, Jeu.hauteur))
        image.fill(BLANC)
        
        blit_centre(image, TITRE_PARAMS, Jeu.pourcentages_coordonees(50, 10, ret_pos=False))
        fin_params : int = Parametre.dessiner_groupe(image, PARAMETRES_NORMAUX)
        
        if params.mode_debug.case_cochee:
            fin_params += 40
            blit_centre(image, TITRE_TRICHE, (Jeu.pourcentage_largeur(50), fin_params))
            fin_params = Parametre.dessiner_groupe(image, PARAMETRES_TRICHE)
            
            fin_params += 40
            pos_bouton : Pos = centrer_pos(
                Pos(Jeu.centre_fenetre[0], fin_params),
                butt_actualisation.rect.size,
                centrer_y=False,
            )
            
            butt_actualisation.change_pos(pos_bouton)
            butt_actualisation.draw(Jeu.menus_surf, point_size=80)
        
        bouton_sortir.draw(image, point_size=0)
        
        try:
            yield image
        except GeneratorExit:
            break
    logging.debug("← Fin interruption (paramètres).")

def lancer_parametres() -> None:
    terminer_interruption(menu_parametres())