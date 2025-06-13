from monstre import *
from Boutton import *
from player import *

def quit(exit_code=0):
    pygame.quit()
    sys.exit(exit_code)

def menu_frame():
    fenetre.fill(BLEU_CLAIR)
    for bouton in bouttons:
        bouton.draw(fenetre)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            check_all_clicks(event.pos)

def change_cursor_pos(evt):
    if event.type != pygame.KEYDOWN or not variables_globales.tour_joueur:
        return

    if evt.key == pygame.K_UP:
        variables_globales.curseur_y = (13 * (HAUTEUR // 16))
    if evt.key == pygame.K_DOWN:
        variables_globales.curseur_y = (13 * (HAUTEUR // 16)) + 70
    if evt.key == pygame.K_LEFT:
        variables_globales.curseur_x = 50
    if evt.key == pygame.K_RIGHT:
        variables_globales.curseur_x = 350

def partie_fin(gagne):
    if gagne:
        fenetre.fill(VERT)
        fenetre.blit(texte_gagner, ((LARGEUR // 2) - 120, HAUTEUR // 2 - 20))
        print("Vous avez gagné !")
    else:
        fenetre.fill(BLEU_CLAIR)
        fenetre.blit(texte_perdu, ((LARGEUR // 2) - 120, HAUTEUR // 2 - 20))
        print("Vous avez perdu...")
    pygame.display.flip()

    time.sleep(2)
    quit()

nouveau_monstre()
while True:
    rafraichir_ecran()
    # clock.tick(60)  # Limite la boucle à 60 FPS # Pas très important (pas de physique)


    while variables_globales.menu_running:
        menu_frame()

    rafraichir_ecran()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN and variables_globales.tour_joueur:
            if event.key == pygame.K_ESCAPE:
                quit()
            if event.key == pygame.K_i:
                afficher_info()
            
            change_cursor_pos(event)

            if event.key == pygame.K_SPACE:
                player_sectionne_attaque()
                variables_globales.tour_joueur = False


    if variables_globales.monstre_vie <= 0:
        # on laisse le joueur avec la vie qu'il avait au combat précédent
        
        variables_globales.nbr_combat += 1

        variables_globales.tour_joueur = True
        
        if variables_globales.nbr_combat >= MAX_COMBAT:
            partie_fin(gagne=True)
        
        # else implicite
        afficher_nombre_combat(variables_globales.nbr_combat)
        nouveau_monstre()

    if not variables_globales.tour_joueur:
        monstre_attaque()
        variables_globales.tour_joueur = True
    
    if variables_globales.joueur_vie <= 0:
        partie_fin(gagne=False)