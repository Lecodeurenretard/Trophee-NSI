from combat import *
from UI import *

def player_heal():
    heal = attaque_soin(variables_globales.perso_stat, 1.5)
    
    variables_globales.joueur_vie = min(variables_globales.joueur_vie + heal, variables_globales.perso_stat["vie"])  # Ne pas dépasser la vie maximale
    update_barre_de_vie_joueur()
    
    pygame.draw.rect(fenetre, NOIR, (400, 300 , 200, 50), 5)
    pygame.display.flip()
    time.sleep(1)

    pygame.event.clear()
    rafraichir_ecran()
    time.sleep(1)

    pygame.event.clear()

def player_attaque_magique():
    degat_magique = degat_infliger_magique(variables_globales.perso_stat, variables_globales.monstre_stat, variables_globales.att_magique_puissance)
    
    if not INVICIBLE_ENNEMI:
        variables_globales.monstre_vie = max(0, variables_globales.monstre_vie - degat_magique)  # Empêche la vie de passer sous 0
        update_barre_de_vie_monstre()
    
    pygame.draw.rect(fenetre, BLEU, (400, 300 , 200, 50), 5)
    pygame.display.flip()
    time.sleep(1)
    
    pygame.event.clear()
    rafraichir_ecran()
    time.sleep(1)
    
    pygame.event.clear()

def player_attaque_physique():
    degat = degat_infliger_physique(variables_globales.perso_stat, variables_globales.monstre_stat, variables_globales.charge_puissance)
    
    if not INVICIBLE_ENNEMI:
        variables_globales.monstre_vie = max(0, variables_globales.monstre_vie - degat)  # Empêche la vie de passer sous 0
        update_barre_de_vie_monstre()
    
    pygame.draw.rect(fenetre, VERT, (400, 300 , 200, 50), 5)
    pygame.display.flip()
    time.sleep(1)
    
    pygame.event.clear()
    rafraichir_ecran()
    time.sleep(1)
    
    pygame.event.clear()

def player_skip_tour():
    pygame.draw.rect(fenetre, ROUGE, (400, 300 , 200, 50), 5)
    pygame.display.flip()
    time.sleep(1)


def player_sectionne_attaque():
    if variables_globales.curseur_x == 50 and variables_globales.curseur_y == (13 * (HAUTEUR // 16)):
        player_heal()
        return
    
    if variables_globales.curseur_x == 350 and variables_globales.curseur_y == (13 * (HAUTEUR // 16)):
        player_attaque_magique()
        return
    
    if variables_globales.curseur_x == 50 and variables_globales.curseur_y == (13 * (HAUTEUR // 16)) + 70:
        player_attaque_physique()
        return
    
    if variables_globales.curseur_x == 350 and variables_globales.curseur_y == (13 * (HAUTEUR // 16)) + 70:
        player_skip_tour()