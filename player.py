from monstre import *
from UI import *

def joueur_dessine_attaque(couleur):
    pygame.draw.rect(fenetre, couleur, (400, 300 , 200, 50), 5)
    pygame.display.flip()
    time.sleep(1)
    
    rafraichir_ecran()
    time.sleep(1)
    
    pygame.event.clear()

def joueur_attaque_soin():
    soin = joueur_calculer_attaque_soin(variables_globales.joueur_stat, 1.5)
    joueur_recoit_degats(-soin) # degats négatifs => soins
    
    joueur_dessine_attaque(VERT)

def joueur_attaque_magique():
    degat_magique = joueur_calculer_degat_magique_inflige(variables_globales.joueur_stat, variables_globales.monstre_stat, variables_globales.att_magique_puissance)
    monstre_recoit_degats(degat_magique)
    
    joueur_dessine_attaque(BLEU)

def joueur_attaque_physique():
    degats = joueur_caluler_degat_physique_inflige(variables_globales.joueur_stat, variables_globales.monstre_stat, variables_globales.charge_puissance)
    monstre_recoit_degats(degats)
    
    joueur_dessine_attaque(ROUGE)

def joueur_skip_tour():
    joueur_dessine_attaque(NOIR)

def joueur_sectionne_attaque():
    curseur_empl = get_curseur_emplacement()

    if curseur_empl == (0, 0):
        joueur_attaque_soin()
        return
    
    if curseur_empl == (1, 0):
        joueur_attaque_magique()
        return
    
    if curseur_empl == (0, 1):
        joueur_attaque_physique()
        return
    
    if curseur_empl == (1, 1):
        joueur_skip_tour()
        return
    
    print(f"Verbose: le curseur est à l'emplacement {curseur_empl} (position {(variables_globales.curseur_x, variables_globales.curseur_y)}).")
    print(f"Verbose: positions x attendues: {variables_globales.curseur_pos_attendue_x[0]} ou {variables_globales.curseur_pos_attendue_x[1]}.")
    print(f"Verbose: positions y attendues: {variables_globales.curseur_pos_attendue_y[0]} ou {variables_globales.curseur_pos_attendue_y[1]}.")
    raise ValueError("Le curseur n'est pas à la bonne position!")