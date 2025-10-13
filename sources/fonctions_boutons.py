from UI import *

def lancer_jeu() -> None:
    logging.info("→ Lancement du jeu...")
    Jeu.changer_etat(Jeu.Etat.ATTENTE_NOUVEAU_COMBAT)
    
    if not param.mode_debug.case_cochee:
        demander_pseudo()
        faux_chargement()
        return
    
    joueur.pseudo = "Testeur"

def menu_parametres() -> Interruption:
    logging.debug("→ Interruption: Paramètres")
    bouton_sortir : Button = Button('X', (10, 10, 50, 50))
    
    TITRE_PARAMS : Surface = Constantes.Polices.TITRE.render("Options de jeu"   , True, NOIR)
    TITRE_TRICHE : Surface = Constantes.Polices.TITRE.render("Options de triche", True, NOIR)
    
    while True:
        for ev in pygame.event.get():
            verifier_pour_quitter(ev)
            
            for parametre in PARAMETRES_NORMAUX:
                parametre.prendre_input(ev)
            
            if param.mode_debug.case_cochee:
                for parametre in PARAMETRES_TRICHE:
                    parametre.prendre_input(ev)
            
            if (
                ev.type == pygame.MOUSEBUTTONDOWN and bouton_sortir.in_butt_hit(ev.pos)
                or ev.type == pygame.KEYDOWN and ev.key == Constantes.Touches.SETTINGS
            ):
                logging.debug("← Fin interruption (paramètres).")
                return
        
        image : Surface = Surface((Jeu.LARGEUR, Jeu.HAUTEUR))
        image.fill(BLANC)
        
        blit_centre(image, TITRE_PARAMS, (Jeu.pourcentage_largeur(50), Jeu.pourcentage_hauteur(10)))
        fin_params : int = Parametre.dessiner_groupe(image, PARAMETRES_NORMAUX)
        
        if param.mode_debug.case_cochee:
            blit_centre(image, TITRE_TRICHE, (Jeu.pourcentage_largeur(50), fin_params + 40))
            Parametre.dessiner_groupe(image, PARAMETRES_TRICHE)
        
        bouton_sortir.draw(image)
        
        yield image

def lancer_parametres() -> None:
    terminer_interruption(menu_parametres())