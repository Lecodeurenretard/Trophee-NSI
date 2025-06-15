from UI import *

def jouer():
    variables_globales.menu_running = False
    chargement()
    variables_globales.pseudo_joueur = demander_pseudo()
    afficher_nombre_combat(variables_globales.nbr_combat)
    

def ouvrir_parametres():
    print("→ Ouverture des paramètres...")
    ...

def afficher_credits():
    texte_credits = variables_globales.police.render("Développé par Jules et Lucas", True, BLANC)
    credit_y = HAUTEUR
    running = False
    while credit_y > 0:
        fenetre.fill(NOIR)
        fenetre.blit(texte_credits, (150, credit_y))
        credit_y -= 1
        pygame.display.flip()
        pygame.time.delay(4)
    print("→ Affichage des crédits...")