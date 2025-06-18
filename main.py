from monstre import *
from Boutton import *
from player import *

def quit(exit_code : int = 0) -> NoReturn:
    pygame.quit()
    sys.exit(exit_code)

def menu_frame() -> None:
    fenetre.fill(BLEU_CLAIR)
    for bouton in bouttons:
        bouton.draw(fenetre)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            check_all_clicks(event.pos)

def change_cursor_pos(evt : pygame.event.Event) -> None:
    if event.type != pygame.KEYDOWN or not variables_globales.tour_joueur:
        return

    if evt.key == pygame.K_UP:
        variables_globales.curseur_y = variables_globales.curseur_pos_attendue_y[0]
    if evt.key == pygame.K_DOWN:
        variables_globales.curseur_y = variables_globales.curseur_pos_attendue_y[1]
    if evt.key == pygame.K_LEFT:
        variables_globales.curseur_x = variables_globales.curseur_pos_attendue_x[0]
    if evt.key == pygame.K_RIGHT:
        variables_globales.curseur_x = variables_globales.curseur_pos_attendue_x[1]

def partie_fin(gagne : bool) -> NoReturn:
    if gagne:
        fenetre.fill(VERT)
        fenetre.blit(TEXTE_VICTOIRE, (LARGEUR // 2 - 120, HAUTEUR // 2 - 20))
        print("Vous avez gagné !")
    else:
        fenetre.fill(BLEU_CLAIR)
        fenetre.blit(TEXTE_DEFAITE, (LARGEUR // 2 - 120, HAUTEUR // 2 - 20))
        print("Vous avez perdu...")
    pygame.display.flip()

    time.sleep(2)
    quit()

nouveau_monstre()
reset_vie_joueur()
while True:
    rafraichir_ecran()
    clock.tick(60)
    
    # Le menu qu'il y a avant le jeu
    while variables_globales.menu_running:
        menu_frame()
    
    rafraichir_ecran()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type != pygame.KEYDOWN or not variables_globales.tour_joueur:
            continue
       
        if event.key == pygame.K_ESCAPE:
            quit()
        if event.key == pygame.K_i:
            afficher_info()
            continue        # Un event ne peut être qu'une seule touche à la fois
        
        if event.key == pygame.K_SPACE:
            joueur_sectionne_attaque()
            variables_globales.tour_joueur = False
            continue
        
        change_cursor_pos(event)
    
    
    if variables_globales.monstre_stat.vie <= 0:
        # on laisse le joueur avec la vie qu'il avait au combat précédent
        
        variables_globales.nbr_combat += 1
        
        variables_globales.tour_joueur = True
        
        if variables_globales.nbr_combat > MAX_COMBAT:
            partie_fin(gagne=True)
        
        # else implicite
        afficher_nombre_combat(variables_globales.nbr_combat)
        nouveau_monstre()
    
    if not variables_globales.tour_joueur:
        monstre_attaque()
        variables_globales.tour_joueur = True
    
    if variables_globales.joueur_stat.vie <= 0:
        partie_fin(gagne=False)