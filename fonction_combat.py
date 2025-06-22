from Monstre import *
from Joueur import *
from UI import *

def joueur_attaque(clef_attaque : str) -> None:
    if len(Monstre.monstres_en_vie) == 0:
        return
    
    if joueur.attaquer(Monstre.monstres_en_vie[0].get_id(), clef_attaque):   # attaque le premier monstre
        del(Monstre.monstres_en_vie[0])     # Si considéré comme mort, le détruit
    
    joueur.dessiner_attaque(fenetre, clef_attaque)
    rafraichir_ecran()
    time.sleep(1)

def joueur_selectionne_attaque():
    curseur_empl : tuple[int|NaN, int|NaN] = get_curseur_emplacement()
    
    if curseur_empl == (0, 0):
        joueur_attaque("heal")
        return
    
    if curseur_empl == (1, 0):
        joueur_attaque("magie")
        return
    
    if curseur_empl == (0, 1):
        joueur_attaque("physique")
        return
    
    if curseur_empl == (1, 1):
        joueur_attaque("skip")
        return
    
    print(f"Verbose: le curseur est à l'emplacement {curseur_empl} (position {(variables_globales.curseur_x, variables_globales.curseur_y)}).")
    print(f"Verbose: positions x attendues: {variables_globales.curseur_pos_attendue_x[0]} ou {variables_globales.curseur_pos_attendue_x[1]}.")
    print(f"Verbose: positions y attendues: {variables_globales.curseur_pos_attendue_y[0]} ou {variables_globales.curseur_pos_attendue_y[1]}.")
    raise ValueError("Le curseur n'est pas à la bonne position!")

def monstre_attaque() -> None:
    attaque_choisie : Attaque = Monstre.monstres_en_vie[0].choisir_attaque()
    Monstre.monstres_en_vie[0].attaquer(joueur.get_id(), attaque_choisie)
    Monstre.monstres_en_vie[0].dessiner_attaque(fenetre, attaque_choisie)