from monstre import *
from Boutton import *


# Fonction bloquante incluse dans la bibliothèque Graphique.py
# permettant de fermer la fenêtre et de stopper le programme

nouveau_monstre()
while True:
    while variables_globales.menu_running:
        fenetre.fill(BLEU_CLAIR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for bouton in boutons:
                    bouton.check_click(event.pos)
        for bouton in boutons:
            bouton.draw(fenetre)
        pygame.display.flip()

    rafraichir_ecran()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and variables_globales.tour_joueur:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_i:
                afficher_info()
            if event.key == pygame.K_UP:
                if variables_globales.curseur_y != (13 * (HAUTEUR // 16)):
                    variables_globales.curseur_y = (13 * (HAUTEUR // 16))
            if event.key == pygame.K_DOWN:
                if variables_globales.curseur_y != (13 * (HAUTEUR // 16)) + 70:
                    variables_globales.curseur_y = (13 * (HAUTEUR // 16)) + 70
            if event.key == pygame.K_LEFT:
                if variables_globales.curseur_x != 50:
                    variables_globales.curseur_x = 50
            if event.key == pygame.K_RIGHT:
                if variables_globales.curseur_x != 350:
                    variables_globales.curseur_x = 350
            if event.key == pygame.K_SPACE:
                if variables_globales.curseur_x == 50 and variables_globales.curseur_y == (13 * (HAUTEUR // 16)):
                    pygame.draw.rect(fenetre, NOIR, (400, 300 , 200, 50), 5)
                    heal = attaque_soin(variables_globales.perso_stat, 1.5)
                    variables_globales.joueur_vie = min(variables_globales.joueur_vie + heal, variables_globales.perso_stat["vie"])  # Ne pas dépasser la vie maximale
                    variables_globales.barre_vie_joueur = pourcentage_vie(variables_globales.joueur_vie, variables_globales.perso_stat["vie"])
                    pygame.display.flip()
                    time.sleep(1)
                    pygame.event.clear()
                    rafraichir_ecran()
                    time.sleep(1)
                    pygame.event.clear()
                elif variables_globales.curseur_x == 350 and variables_globales.curseur_y == (13 * (HAUTEUR // 16)):
                    pygame.draw.rect(fenetre, BLEU, (400, 300 , 200, 50), 5)
                    degat_magique = degat_infliger_magique(variables_globales.perso_stat, variables_globales.monstre_stat, variables_globales.att_magique)
                    variables_globales.monstre_vie = max(0, variables_globales.monstre_vie - degat_magique)  # Empêche la vie de passer sous 0
                    variables_globales.barre_vie_adversaire = pourcentage_vie(variables_globales.monstre_vie, variables_globales.monstre_stat["vie"])
                    pygame.display.flip()
                    time.sleep(1)
                    pygame.event.clear()
                    rafraichir_ecran()
                    time.sleep(1)
                    pygame.event.clear()
                elif variables_globales.curseur_x == 50 and variables_globales.curseur_y == (13 * (HAUTEUR // 16)) + 70:
                    pygame.draw.rect(fenetre, VERT, (400, 300 , 200, 50), 5)
                    variables_globales.degat = degat_infliger_physique(variables_globales.perso_stat, variables_globales.monstre_stat, variables_globales.charge)
                    variables_globales.monstre_vie = max(0, variables_globales.monstre_vie - variables_globales.degat)  # Empêche la vie de passer sous 0
                    variables_globales.barre_vie_adversaire = pourcentage_vie(variables_globales.monstre_vie, variables_globales.monstre_stat["vie"])
                    pygame.display.flip()
                    time.sleep(1)
                    pygame.event.clear()
                    rafraichir_ecran()
                    time.sleep(1)
                    pygame.event.clear()
                elif variables_globales.curseur_x == 350 and variables_globales.curseur_y == (13 * (HAUTEUR // 16)) + 70:
                    pygame.draw.rect(fenetre, ROUGE, (400, 300 , 200, 50), 5)
                    pygame.display.flip()
                    time.sleep(1)
                variables_globales.tour_joueur = False


    if variables_globales.monstre_vie <= 0 and variables_globales.nbr_combat > 4:
        fenetre.fill(BLANC)
        fenetre.blit(texte_gagner, ((LARGEUR // 2) - 120, HAUTEUR // 2 - 20))
        pygame.display.flip()
        print("Vous avez gagné !")
        time.sleep(2)
        pygame.quit()
        sys.exit()
    elif variables_globales.monstre_vie <= 0:
        variables_globales.nbr_combat += 1
        afficher_nombre_combat(variables_globales.nbr_combat)
        nouveau_monstre()
        variables_globales.barre_vie_adversaire = pourcentage_vie(variables_globales.monstre_vie, variables_globales.monstre_stat["vie"])
        variables_globales.barre_vie_joueur = pourcentage_vie(variables_globales.joueur_vie, variables_globales.perso_stat["vie"])
        variables_globales.tour_joueur = True

    if not variables_globales.tour_joueur:
        monstre_attaque()
        variables_globales.tour_joueur = True
        if variables_globales.joueur_vie <= 0:
            fenetre.fill(BLANC)
            fenetre.blit(texte_perdu, ((LARGEUR // 2) - 120, HAUTEUR // 2 - 20))
            pygame.display.flip()
            print("Vous avez gagné !")
            time.sleep(2)
            pygame.quit()
            sys.exit()

    
    rafraichir_ecran()
    clock.tick(60)  # Limite la boucle à 60 FPS

