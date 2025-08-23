from UI import *

def lancer_jeu() -> None:
    globales.menu_running = False
    if not MODE_DEBUG:
        demander_pseudo()
        chargement()
        afficher_nombre_combat(globales.nbr_combat)
        return
    afficher_nombre_combat(globales.nbr_combat)
    joueur.pseudo = "Testeur"

def ouvrir_parametres() -> None:
    logging.info("→ Ouverture des paramètres...")
    pass

def afficher_credits() -> None:
    logging.info("→ Affichage des crédits...")
    texte_credits : Surface = globales.POLICE_FOURRE_TOUT.render("Développé par Jules et Lucas", True, BLANC)
    credit_y : int = HAUTEUR
    
    while credit_y > 0:
        verifier_pour_quitter()
        fenetre.fill(NOIR)
        fenetre.blit(texte_credits, (150, credit_y))
        
        credit_y -= 1
        
        pygame.display.flip()
        pygame.time.delay(4)