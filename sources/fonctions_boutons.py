from UI import *

def menu_parametres() -> Interruption:
    logging.debug("→ Interruption: Paramètres")
    bouton_sortir : Button = Button((10, 10, 50, 50), img=f"{Constantes.Chemins.IMG}/croix.png")
    
    TITRE_PARAMS : Surface = Constantes.Polices.TITRE.render("Options de jeu"   , True, NOIR)
    TITRE_TRICHE : Surface = Constantes.Polices.TITRE.render("Options de triche", True, NOIR)
    
    while True:
        continuer : bool = True
        for ev in pygame.event.get():
            verifier_pour_quitter(ev)
            
            for parametre in PARAMETRES_NORMAUX:
                parametre.prendre_input(ev)
            
            if params.mode_debug.case_cochee:
                for parametre in PARAMETRES_TRICHE:
                    parametre.prendre_input(ev)
            
            if (
                ev.type == pygame.MOUSEBUTTONDOWN and bouton_sortir.in_butt_hit(ev.pos)
                or ev.type == pygame.KEYDOWN and ev.key == Constantes.Touches.SETTINGS
            ):
                continuer = False
                break
        if not continuer:
            break
        
        image : Surface = Surface((Jeu.largeur, Jeu.hauteur))
        image.fill(BLANC)
        
        blit_centre(image, TITRE_PARAMS, Jeu.pourcentages_coordonees(50, 10))
        fin_params : int = Parametre.dessiner_groupe(image, PARAMETRES_NORMAUX)
        
        if params.mode_debug.case_cochee:
            blit_centre(image, TITRE_TRICHE, (Jeu.pourcentage_largeur(50), fin_params + 40))
            Parametre.dessiner_groupe(image, PARAMETRES_TRICHE)
        
        bouton_sortir.draw(image)
        
        try:
            yield image
        except GeneratorExit:
            break
    logging.debug("← Fin interruption (paramètres).")

def lancer_parametres() -> None:
    terminer_interruption(menu_parametres())