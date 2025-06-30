from Monstre import *
from Joueur import *
from UI import *

def joueur_attaque(clef_attaque : str) -> None:
    if len(Monstre.monstres_en_vie) == 0:
        return
    
    crit = joueur.attaquer(Monstre.monstres_en_vie[0].get_id(), clef_attaque)   # attaque le premier monstre
    joueur.dessiner_attaque(fenetre, clef_attaque, crit)
    
    rafraichir_ecran()
    time.sleep(1)

def joueur_selectionne_attaque():
    curseur_menu_empl : tuple[int, int] = curseur_menu_combat.get_position_dans_position()
    
    if curseur_menu_empl == (0, 0):
        joueur_attaque("heal")
        return
    
    if curseur_menu_empl == (1, 0):
        joueur_attaque("magie")
        return
    
    if curseur_menu_empl == (0, 1):
        joueur_attaque("physique")
        return
    
    if curseur_menu_empl == (1, 1):
        joueur_attaque("skip")
        return
    
    raise ValueError(f"Le curseur du menu est à une position imprévue ({curseur_menu_empl} dans ses positions possibles)!")

def monstre_attaque() -> None:
    attaque_choisie : Attaque = Monstre.monstres_en_vie[0].choisir_attaque()
    crit = Monstre.monstres_en_vie[0].attaquer(joueur.get_id(), attaque_choisie)
    Monstre.monstres_en_vie[0].dessiner_attaque(fenetre, attaque_choisie, crit)