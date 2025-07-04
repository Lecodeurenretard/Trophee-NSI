from UI import *

def jouer() -> None:
    variables_globales.menu_running = False
    if MODE_DEBUG:
        joueur.set_pseudo("Testeur")
    else:
        chargement()
        demander_pseudo()
    afficher_nombre_combat(variables_globales.nbr_combat)

def ouvrir_parametres() -> None:
    print("→ Ouverture des paramètres...")

def afficher_credits() -> None:
    print("→ Affichage des crédits...")
    texte_credits : Surface = variables_globales.police.render("Développé par Jules et Lucas", True, BLANC)
    credit_y : int = HAUTEUR
    
    while credit_y > 0:
        fenetre.fill(NOIR)
        fenetre.blit(texte_credits, (150, credit_y))
        
        credit_y -= 1
        
        pygame.display.flip()
        pygame.time.delay(4)