from fonctions_main import *
from import_local import *

def lancer_jeu() -> None:
    logging.info("→ Lancement du jeu...")
    globales.menu_running = False
    
    if not param.mode_debug.case_cochee:
        demander_pseudo()
        faux_chargement()
        nouveau_combat(1, True)
        return
    
    joueur.pseudo = "Testeur"
    nouveau_combat(1, True)

def menu_parametres() -> Interruption:
    logging.info("→ Ouverture des paramètres...")
    bouton_sortir : Button = Button('X', (10, 10, 50, 50))
    
    TITRE_PARAMS : Surface = POLICE_TITRE.render("Options de jeu", True, NOIR)
    TITRE_TRICHE : Surface = POLICE_TITRE.render("Options de triche", True, NOIR)
    
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
                or ev.type == pygame.KEYDOWN and ev.key == UI_TOUCHE_SETTINGS
            ):
                logging.info("← Fermeture des paramètres.")
                return
        
        image : Surface = Surface((LARGEUR, HAUTEUR))
        image.fill(BLANC)
        
        blit_centre(image, TITRE_PARAMS, (pourcentage_largeur(50), pourcentage_hauteur(10)))
        fin_params : int = Parametre.dessiner_groupe(image, PARAMETRES_NORMAUX)
        
        if param.mode_debug.case_cochee:
            blit_centre(image, TITRE_TRICHE, (pourcentage_largeur(50), fin_params + 40))
            Parametre.dessiner_groupe(image, PARAMETRES_TRICHE)
        
        bouton_sortir.draw(image)
        
        yield image

def lancer_parametres() -> None:
    terminer_interruption(menu_parametres())

def afficher_credits() -> None:
    logging.info("→ Affichage des crédits...")
    texte_credits : Surface = globales.POLICE_FOURRE_TOUT.render("Développé par Jules et Lucas", True, BLANC)
    credit_y : int = HAUTEUR
    
    while credit_y > 0:
        verifier_pour_quitter()
        fenetre.fill(NOIR)
        blit_centre(fenetre, texte_credits, (pourcentage_largeur(50), credit_y))
        
        credit_y -= 1
        
        pygame.display.flip()
        pygame.time.delay(4)